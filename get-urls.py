import aiohttp
import json,os
from DataRecorder import Recorder
import asyncio

proxy_url=None
domain = os.getenv("domain")

#domain='toolify.ai'
#domain='claude.site'
#domain='revved.com'
#domain='https://www.amazon.com/sp?ie=UTF8&seller='
no_subs=None
subs_wildcard = "*." if not no_subs else ""
# subs_wildcard=''
domainname = domain.replace("https://", "")
domainname=domainname.split('/')[0]
outfile=Recorder(f'result/waybackmachines-{domainname}.csv')
output_folder='output'
folder_path='result'
query_url = f"http://web.archive.org/cdx/search/cdx?url={subs_wildcard}{domain}/&fl=timestamp,original,mimetype,statuscode,digest'"

# query_url='https://web.archive.org/__wb/sparkline?output=json&url=toolify.ai&collection=web'
headers = {'Referer': 'https://web.archive.org/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/92.0.4515.107 Safari/537.36'}
# initialize an AIOHTTP client with the SOCKS proxy connector
async def getdata():
    async with aiohttp.ClientSession(connector=None) as session:
    # Perform your web requests using the session
        try:
            resp=await session.get(query_url,
                               headers=headers)
            raw=await resp.text()
            print(raw)
            if resp.status != 200:
            # Handle different HTTP status codes
            # return 
                print('not 200')
        # Process the response
            lines = raw.splitlines()
            print(len(lines))
            for line in lines:
                parts = line.split(' ', 2)
                timestamp, original_url = parts[0], parts[1]
                outfile.add_data({'date':timestamp,'url':original_url})
            return True
        except aiohttp.ClientError as e:
            print(f"Connection error: {e}", 'red')
        except Exception as e:
            print(f"Couldn't get list of responses: {e}", 'red')
        # out.append(Wurl(urls[1], urls[2]))
    # return out
        outfile.record()

import os
import shutil
import zipfile

def zip_folder(folder_path, output_folder, max_size_mb, zip_file, zip_temp_file, zip_count):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Convert the maximum size from MB to bytes
    max_size_bytes = max_size_mb * 1024 * 1024

    # Initialize the size of the current zip file
    current_zip_size = 0

    # Iterate over the directory tree
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if adding the next file would exceed the maximum size
            if current_zip_size + os.path.getsize(file_path) > max_size_bytes:
                # Close the current ZIP archive
                zip_file.close()

                # Move the current ZIP file to the output folder
                final_zip_path = os.path.join(output_folder, f"archive{zip_count}.zip")
                shutil.move(zip_temp_file, final_zip_path)

                print(f"Created '{final_zip_path}' (size: {os.path.getsize(final_zip_path)} bytes)")

                # Reset the current zip size and create a new ZIP archive
                current_zip_size = 0
                zip_count += 1
                zip_temp_file = os.path.join(output_folder, f"temp{zip_count}.zip")
                zip_file = zipfile.ZipFile(zip_temp_file, "w", zipfile.ZIP_DEFLATED)

            # Add each file to the current ZIP archive
            zip_file.write(file_path)
            # Update the size of the current zip file
            current_zip_size += os.path.getsize(file_path)

    # Close the last ZIP archive after all files have been added
    zip_file.close()

    # Move the last ZIP file to the output folder
    final_zip_path = os.path.join(output_folder, f"archive{zip_count}.zip")
    shutil.move(zip_temp_file, final_zip_path)

    print(f"Created '{final_zip_path}' (size: {os.path.getsize(final_zip_path)} bytes)")
async def main():


    max_size_mb = 1500
    zip_count = 1
    zip_temp_file = os.path.join(output_folder, f"temp{zip_count}.zip")
    zip_file = zipfile.ZipFile(zip_temp_file, "w", zipfile.ZIP_DEFLATED)
    r=await getdata()
    if r:
      zip_folder(folder_path, output_folder, max_size_mb, zip_file,zip_temp_file,zip_count)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

