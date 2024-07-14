import aiohttp
import asyncio
import csv,os
import time
from aiohttp_socks import ProxyType, ProxyConnector

import shutil
import zipfile
proxy_url = 'socks5://127.0.0.1:1080'  # 填写你的代理服务器地址
proxy_url=None
domain = 'https://www.amazon.com/stores/'  # 你的域名
domain='sellercenter.amazon.com'

async def geturls(domain):
    no_subs=None
    subs_wildcard = "*." if not no_subs else ""
    # subs_wildcard=''
    domainname = domain.replace("https://", "")
    domainname=domainname.split('/')[0]
    csv_file = f'./result/waybackmachines-{domainname}.csv'

    query_url = f"http://web.archive.org/cdx/search/cdx?url={subs_wildcard}{domain}/&fl=timestamp,original,mimetype,statuscode,digest"
    query_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/&matchType=prefix&fl=timestamp,original"
    fileter='&statuscode=200'
    filter="&collapse=urlkey"
    query_url=query_url+filter
    query_url=query_url+'&matchType=prefix'

    # For example: http://web.archive.org/cdx/search/cdx?url=archive.org&from=2010&to=2011



    # query_url='https://web.archive.org/__wb/sparkline?output=json&url=toolify.ai&collection=web'
    # connector = ProxyConnector.from_url(proxy_url)
    headers = {'Referer': 'https://web.archive.org/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/92.0.4515.107 Safari/537.36'}
    # initialize an AIOHTTP client with the SOCKS proxy connector
    async with aiohttp.ClientSession(connector=None) as session:
        # Perform your web requests using the session
        try:
            resp=await session.get(query_url,
                                headers=headers,
                # auth=auth.prepare_request, 
                # proxy='http://127.0.0.1:1080',
                timeout=300000)     
            count=0
            while True:
                raw = await resp.content.read(10240)  # 每次读取1024字节
                if not raw:
                    break
                # raw=await resp.text()
                # print(raw)
                try:

                    raw = raw.decode('utf-8')
                except UnicodeDecodeError:
                    raw = raw.decode('latin-1')

                if resp.status != 200:
                # Handle different HTTP status codes
                # return 
                    print('not 200')
            # Process the response
                # print(raw)
                lines = raw.splitlines()
                fieldnames = ['date', 'url']

                print(len(lines))
                count=count+len(lines)
                file_exists = os.path.isfile(csv_file)
                for line in lines:
                    
                    if ' ' in line:
                        try:
                            timestamp, original_url = line.strip().split(' ', 1)
                            data = {'date': timestamp, 'url': original_url}

                            with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                                writer = csv.DictWriter(f, fieldnames=['date', 'url'])
                                # if not file_exists:
                                    # writer.writeheader()
                                # print('add 1')
                                writer.writerow(data)
                                file_exists = True
                            count += 1
                        except Exception as e:
                            print(f"Error processing line: {e}")
                print('till now',count)
            print(f"Total URLs processed: {count}")

        except aiohttp.ClientError as e:
            print(f"Connection error: {e}", 'red')
            await geturls( domain)

        except Exception as e:
            print(f"Couldn't get list of responses: {e}", 'red')
            await geturls( domain)
        # return out
async def main(domain):
    retries = 5
    for i in range(retries):
        try:

            await geturls(domain)
            break  # 如果成功，则退出循环
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Connection error on attempt {i+1}: {e}")
            if i < retries - 1:
                await asyncio.sleep(2**i)  # 指数退避策略
            else:
                print("Max retries reached. Exiting.")
                return

def zip_folder(
    folder_path, output_folder, max_size_mb, zip_file, zip_temp_file, zip_count
):
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

                print(
                    f"Created '{final_zip_path}' (size: {os.path.getsize(final_zip_path)} bytes)"
                )

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


if __name__ == "__main__":
    folder_path = "./result"

    if os.path.exists(folder_path) == False:
        os.mkdir(folder_path)

    output_folder = "./output" 

    # Check if the directory exists
    if not os.path.exists(output_folder):
        # If the directory does not exist, create it
        os.mkdir(output_folder)
    print("Directory 'output' was created.")   
    start_time = time.time()
    asyncio.run(main(domain))
    print(f"Time taken for asynchronous execution: {time.time() - start_time} seconds")
    # Specify the maximum size of each RAR file in MB
    max_size_mb = 1500

    # Create a temporary ZIP file for the first archive
    zip_count = 1
    zip_temp_file = os.path.join(folder_path, f"temp{zip_count}.zip")
    zip_file = zipfile.ZipFile(zip_temp_file, "w", zipfile.ZIP_DEFLATED)

    # Compress the folder into multiple ZIP archives
    zip_folder(
        folder_path, output_folder, max_size_mb, zip_file, zip_temp_file, zip_count
    )
