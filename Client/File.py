from os.path import exists
from numpy import array_split, array
import requests
import json
from time import sleep


class File:
    parts = []
    keys = []
    num_of_parts = 0
    redundancy = 0
    file_path = ''

    # Create a file object
    def __init__(self, file_path, keys, num_of_parts, redundancy):
        self.file_path = file_path
        self.keys = keys
        self.num_of_parts = num_of_parts
        self.redundancy = redundancy

    # Converts the file to binary
    def _convert_to_binary(self):

        # Check to see if file exists
        if exists(self.file_path):
            bytes = []

            # Read in file and get all the bytes
            with open(self.file_path, "rb") as file:
                byte = file.read(1)
                while byte:
                    bytes.append(byte)
                    byte = file.read(1)

            return bytes
        else:
            print("File does not exist")
            return

    # Returns parts of a file
    def _spit_into_parts(self, bytes, num_of_parts):

        parts = []

        split_array = array_split(array(bytes), num_of_parts)

        for i in range(len(split_array)):

            hashable = ""
            # convert the array of bytes into a string
            for byte in split_array[i]:
                hashable += str(byte)

            part = Part(split_array[i], self._generate_id(hashable))
            parts.append(part)

        return parts

    # Generates id fby hashing the data in a part
    def _generate_id(self, arr):
        return hash(arr)

    # Encrypt each part
    def _encrypt_parts(self, parts, keys):
        #TODO encypt parts
        return parts

    # Returns an uploaded file
    def upload(self, master_node_ip="10.0.0.9:8080"):

        bytes = self._convert_to_binary()
        parts = self._spit_into_parts(bytes, self.num_of_parts)
        encrypted_parts = self._encrypt_parts(parts, self.keys)


        params = {'amount': self.num_of_parts * (self.redundancy + 1)}

        master_node_ip = "http://" + master_node_ip
        response = requests.get(url=master_node_ip + "/getnodes", params=params)

        host_ips = response.text.replace("[", "").replace("]", "").replace("\'", "").strip().split(",")

        print("Nodes Received: ", end="")
        print(host_ips)


        all_hosts = []

        # Create Hosts
        for ip in host_ips:
            host = Host(ip)
            all_hosts.append(host)

        hosts = []
        for i in range(self.num_of_parts):
            hosts.append(all_hosts.pop())

        #hosts = [Host("http://10.0.0.10:8080"), Host("http://10.0.0.11:8080"), Host("http://10.0.0.12:8080"), Host("http://10.0.0.13:8080")]

        # An array of arrays of length of parts example
        redundant_hosts_arry = []
        for i in range(self.redundancy):
            redundant_row = []
            for i in range(self.num_of_parts):
                redundant_row.append(all_hosts.pop())
            redundant_hosts_arry.append(redundant_row)



        # [1, 2, 3], [1, 2, 3], [1, 2, 3]
        # Where the length of parts is 3
        #redundant_hosts_arry = [[Host("http://10.0.0.10:8080"), Host("http://10.0.0.11:8080"), Host("http://10.0.0.12:8080"), Host("http://10.0.0.13:8080")]]


        ids = []

        # Upload a part to each host
        for part, host in zip(encrypted_parts, hosts):
            host.upload_part(part)
            ids.append(part.id)

        for redundant_hosts in redundant_hosts_arry:
            for part, host in zip(encrypted_parts, redundant_hosts):
                host.upload_part(part)
        uploaded_file = UploadedFile(self.file_path, ids, self.keys, hosts, redundant_hosts_arry)

        print("Part Ids:", uploaded_file.part_ids)

        return uploaded_file


class Part:
    # Id of the part. Used to download from the host.
    id = ''

    # Data of the file
    data = ''

    def __init__(self, data, id):
        self.data = data
        self.id = id
        pass


class UploadedFile:
    file_name = ''
    hosts = []
    redundant_hosts = []
    part_ids = []
    keys = []

    def __init__(self, file_name, part_ids, keys, hosts, redundant_hosts):
        self.file_name = file_name
        self.part_ids = part_ids
        self.keys = keys
        self.hosts = hosts
        self.redundant_hosts = redundant_hosts
        pass

    # Returns a DownloadedFile object
    def download(self):
        downloaded_parts = []
        for part_index, (part_id, host) in enumerate(zip(self.part_ids, self.hosts)):
            # TODO check if host is online if the host is offline than get the redundant host and download from there
            part = host.download_part(part_id)
            if not part == False:
                downloaded_parts.append(part)
            else:
                print("Node offline trying redundant hosts")
                downloaded_part = False
                # Node Offline get from redundant node
                for row in self.redundant_hosts:
                    # Try to get from redundant host
                    redundant_host = row[part_index]
                    part = redundant_host.download_part(part_id)
                    if not part == False:
                        downloaded_parts.append(part)
                        downloaded_part = True
                        break
                    else:
                        continue

                if downloaded_part:
                    # Yay
                    pass
                else:
                    # :(
                    # Can not complete download
                    return None

        downloaded_file = DownloadedFile(downloaded_parts, self.keys, len(self.part_ids), self.file_name)

        return downloaded_file

    def serialize(self, location=""):

        host_ips = []
        redundant_host_ips = []

        for host in self.hosts:
            host_ips.append(host.ip)

        for redundant_host in self.redundant_hosts:
            redundant_ips_row = []
            for host in redundant_host:
                redundant_ips_row.append(host.ip)
            redundant_host_ips.append(redundant_ips_row)


        output = {
            "file_name": self.file_name,
            "hosts": host_ips,
            "redundant_hosts": redundant_host_ips,
            "part_ids": self.part_ids,
            "keys": self.keys
        }

        path = location + str(self.file_name) + ".uploaded"
        if not location == "" and str(self.file_name).__contains__("/"):
            split_file_name = str(self.file_name).split("/")
            path = location + split_file_name[len(split_file_name)-1] + ".uploaded"

        with open(path, "w") as output_file:
            json.dump(output, output_file)

    @staticmethod
    def load(file_name):

        with open(file_name, "r") as input_file:
            input = input_file.readlines()
            json_in = json.loads(input.pop())

            hosts = []
            for ip in json_in['hosts']:
                hosts.append(Host(ip))

            redundant_hosts = []
            for row in json_in['redundant_hosts']:
                redundant_hosts_row = []
                for ip in row:
                    redundant_hosts_row.append(Host(ip))
                redundant_hosts.append(redundant_hosts_row)


            uploaded_file = UploadedFile(json_in['file_name'], json_in['part_ids'], json_in['keys'], hosts, redundant_hosts)
            return uploaded_file



class DownloadedFile:
    parts = []
    keys = []
    num_of_parts = 0
    file_name = ""

    def __init__(self, parts, keys, num_of_parts, file_name):
        self.parts = parts
        self.keys = keys
        self.num_of_parts = num_of_parts
        self.file_name = file_name
        pass

    def _decrypt_parts(self):
        # TODO decrypt parts
        pass

    def _combine_parts(self):

        combined_data = []

        for part in self.parts:
            for d in part.data:
                combined_data.append(d)

        return combined_data

    def _convert_from_binary(self, bytes, file_name):
        with open(file_name, "wb") as file:
            for b in bytes:
                file.write(b)

        return

    def get_file(self, path):

        if not path == "" and str(self.file_name).__contains__("/"):
            path = path + str(self.file_name).split("/")[1]
        else:
            path = self.file_name

        self._decrypt_parts()
        new_bytes = self._combine_parts()
        print(self.file_name)
        self._convert_from_binary(new_bytes, self.file_name)


# This represents a host that is storing a part of a file
class Host:
    ip = ""

    def __init__(self, ip):
        self.ip = ip
        pass

    def upload_part(self, part):
        params = {'id': part.id, 'data': part.data}
        response = requests.get(url=self.ip+"/upload", params=params)
        if response:
            return True
        else:
            return False

    def download_part(self, part_id):
        try:
            params = {'id': part_id}
            response = requests.get(url=self.ip + "/download", params=params)
            print(response.text)
            data = json.loads(response.text)['data']

            bytes = []
            for char in data:
                bytes.append(str.encode(char))

            part = Part(bytes, part_id)
            return part
        except requests.exceptions.ConnectTimeout:
            return False
        except json.decoder.JSONDecodeError:
            return False


def test_upload():
    keys = []

    file = File("../Surfaces LIVE _ Presented by Grubhub Sound Bites-oH1dTVrFi_Q.webm", keys, 4, 2)
    file = File("../qwerty", keys, 4, 1)


    uploaded_file = file.upload()

    uploaded_file.serialize("./Uploads/")


def test_download():
    uploaded_file = UploadedFile.load("./Uploads/qwerty.uploaded")

    downloaded_file = uploaded_file.download()
    downloaded_file.get_file("./Uploads/")


if __name__ == "__main__":
    test_upload()
