import aiohttp
import asyncio
import csv,os
import time
from aiohttp_socks import ProxyType, ProxyConnector

import shutil
import zipfile
proxy_url = 'socks5://127.0.0.1:1080'  # 填写你的代理服务器地址
domain = 'https://www.amazon.com/sp?'  # 你的域名

async def geturls(session, domain):
    no_subs = None
    subs_wildcard = "*." if not no_subs else ""
    domainname = domain.replace("https://", "").split('/')[0]
    csv_file =f'./result/waybackmachines-{domainname}.csv'

    headers = {
        'Referer': 'https://web.archive.org/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    query_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&fl=timestamp,original"
    filter="&collapse=urlkey"
    query_url=query_url+filter
    # query_url=query_url+'&limit=10'

    try:

        async with session.get(query_url, headers=headers,
                                #  proxy='http://127.0.0.1:1080', 
                                timeout=30000) as resp:
            if resp.status != 200:
                print(f"Failed to get data, status: {resp.status}")
                return

            count = 0
            file_exists = os.path.isfile(csv_file)

            # 使用 iter_any 替代 iter_lines
            # async for chunk in resp.content.iter_any():
            async for chunk in resp.content.iter_chunked(1024):

                if isinstance(chunk, str):
                    lines = chunk.splitlines()
                elif isinstance(chunk, bytes):
                    lines = chunk.decode('utf-8', errors='ignore').splitlines()
                else:
                    continue

                for line in lines:
                    if ' ' in line:
                        try:
                            timestamp, original_url = line.strip().split(' ', 1)
                            data = {'date': timestamp, 'url': original_url}

                            with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                                writer = csv.DictWriter(f, fieldnames=['date', 'url'])
                                if not file_exists:
                                    writer.writeheader()
                                writer.writerow(data)
                                file_exists = True
                            count += 1
                        except Exception as e:
                            print(f"Error processing line: {e}")

            print(f"Total URLs processed: {count}")

    except aiohttp.ClientError as e:
        print(f"Connection error: {e}")
        # 可以在这里添加重试逻辑
        # if 需要重试的条件:
        #     await asyncio.sleep(重试等待时间)
        #     await geturls(session, domain)
    except asyncio.TimeoutError:
        print("The request timed out")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def main(domain):
    retries = 5
    for i in range(retries):
        try:
            connector = ProxyConnector.from_url(proxy_url) if proxy_url else None

            async with aiohttp.ClientSession(connector=None) as session:
                await geturls(session, domain)
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
    import os

# 假设 domainname 变量已经被赋值
    domainname = domain.replace("https://", "").split('/')[0]

# 构建 CSV 文件的完整路径
    csv_file_path = f'./result/waybackmachines-{domainname}.csv'

# 检查 CSV 文件是否存在
    if os.path.exists(csv_file_path):
        print(f"The file '{csv_file_path}' exists.")
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
    else:
        print(f"The file '{csv_file_path}' does not exist.")
