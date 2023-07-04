import hashlib
import os
import subprocess
import requests


def main():
  
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    respond = requests.get(url)
    respond.raise_for_status()
    sha256_file_content = respond.text
    expected_sha256 = sha256_file_content.split()[0]
    return expected_sha256

def download_installer():
    url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp = requests.get(url)
    resp.raise_for_status()
    installer_data = resp.content
    return installer_data

def installer_ok(installer_data, expected_sha256):
    sha256_hash = hashlib.sha256(installer_data).hexdigest()
    return sha256_hash == expected_sha256
    # TODO: Step 3
    #calculate sha256hash value
    #print the hash value
    # Hint: See example code in lab instructions entitled "Computing the Hash Value of a Response Message Body"

def save_installer(installer_data):
    """Saves the VLC installer to a local directory.

    Args:
        installer_data (bytes): VLC installer file binary data

    Returns:
        str: Full path of the saved VLC installer file
    """
   
    # TODO: Step 4
    #check wether the download was successful
    temp_folder = os.getenv('TEMP')
    installer_path = os.path.join(temp_folder, 'vlcinstaller.exe')
    with open(installer_path, 'wb') as file:
        file.write(installer_data)
    return installer_path



def run_installer(installer_path):
    """Silently runs the VLC installer.

    Args:
        installer_path (str): Full path of the VLC installer file
    """    
    # TODO: Step 5
    subprocess.run([installer_path, '/L=1033', '/s'], check=True)
    # Hint: See example code in lab instructions entitled "Running the VLC Installer"
    return
    
def delete_installer(installer_path):
     os.remove(installer_path)


if __name__ == '__main__':
    main()