import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
import json,os
from DataRecorder import Recorder
import csv
import asyncio
proxy_url=None
domain='toolify.ai'
domain='claude.site'
domain='revved.com'
domain='https://www.amazon.com/sp?ie=UTF8&seller='
domain='https://www.amazon.com/sp?'
domain='https://www.amazon.com/sp?_encoding=UTF8&marketplaceID=ATVPDKIKX0DER&orderID=&seller='
domain='https://www.amazon.com/sp?_encoding=UTF8&marketplaceID='
domain='youtube.com'
domains=['https://www.tiktok.com/tag']
domains=['https://www.tiktok.com/@']

# domain='https://www.amazon.com/s'
# domain='https://www.amazon.com/sp?ie=UTF8&seller='

#google search  
#site:tiktok.com/tag/

# site:tiktok.com/tag/ after:2024-07-01 before:2024-08-01
def process_line(csv_file,lines):
    fieldnames = ['timestamp', 'url']

    file_exists = os.path.isfile(csv_file)
    if not file_exists:

        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    for line in lines:
        try:
            if ' ' in line:
                line=str(line).strip()
                parts = line.split(' ')
                timestamp, original_url = parts[0], parts[1]
                    
                data={'timestamp':timestamp,'url':original_url}
                with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    # if not file_exists:
                        # writer.writeheader()
                    writer.writerow(data)
        except:
            print('failed to save',line)
async def geturls(domain,start,end):
    no_subs=None
    subs_wildcard = "*." if not no_subs else ""
    # subs_wildcard=''
    domainname = domain.replace("https://", "")
    domainname=domainname.split('/')[0]
    csv_file=f'result/waybackmachines-{domainname}-user.csv'
    outfile=Recorder(f'waybackmachines-{domainname}.csv')

    query_url = f"http://web.archive.org/cdx/search/cdx?url={subs_wildcard}{domain}/&fl=timestamp,original,mimetype,statuscode,digest"
    query_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&fl=timestamp,original"
    # fileter='&statuscode=200'
    filter="&collapse=digest"
    filter="&collapse=urlkey"
    fileter=None
    if not end: 
        fileter=f'&statuscode=200&from={start}'
    else:
        fileter=f'&statuscode=200&from={start}&to={end}'

    filter="&collapse=urlkey"+fileter
    query_url=query_url+filter

    # query_url=query_url+'&matchType=prefix'
    # query_url=query_url+'&from=2024&to=2024'

    # For example: http://web.archive.org/cdx/search/cdx?url=archive.org&from=2010&to=2011



    # query_url='https://web.archive.org/__wb/sparkline?output=json&url=toolify.ai&collection=web'
    # connector = ProxyConnector.from_url(proxy_url)
    headers = {'Referer': 'https://web.archive.org/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/92.0.4515.107 Safari/537.36'}
    # initialize an AIOHTTP client with the SOCKS proxy connector
    print('start to query',query_url)
    try:
        async with aiohttp.ClientSession(connector=None) as session:
            async with session.get(query_url,
                                   headers=headers,
                                   proxy='http://127.0.0.1:1080',
                                   timeout=300000) as resp:
                print(resp.status, query_url)
                if resp.status != 200:
                    print(f"Received status code {resp.status}.")
                    return

                count = 0
                buffer = bytearray()  # Buffer to store partial read data
                while True:
                    chunk = await resp.content.read(1024)  # Read 1024 bytes chunk
                    if not chunk:
                        # No more data, process remaining buffer
                        if buffer:
                            process_line(csv_file, [buffer.decode('utf-8', 'replace')])
                        break
                    
                    buffer.extend(chunk)  # Append new data to buffer
                    
                    # Process complete lines in the buffer
                    raw = buffer.decode('utf-8', 'replace')
                    lines = raw.splitlines(True)
                    for line in lines[:-1]:  # Process all complete lines
                        process_line(csv_file, [line])
                    
                    buffer = bytearray(lines[-1], 'utf-8')  # Keep the last potentially incomplete line
                    
                    # Example: Print progress
                    count += len(lines)
                    print(f"Processed {count} lines so far...")
    
    except aiohttp.ClientError as e:
        print(f"Connection error: {e}")
        print('start to query',query_url)

    except Exception as e:
        print(f"Error fetching data: {e}")
            # out.append(Wurl(urls[1], urls[2]))
        # return out
        # return out
        print('start to query',query_url)

        outfile.record()
import time
start_time = time.time()
async def one(domain,start,end):
    retries = 5
    for i in range(retries):
        try:

            await geturls(domain,start,end)
            break  # 如果成功，则退出循环
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"{start}-{end} Connection error on attempt {i+1}: {e}")
            
            if i < retries - 1:
                await asyncio.sleep(20*i*(i+1))  # 指数退避策略
            else:
                print("Max retries reached. Exiting.")
                return
async def main():

    # Start and end years
    start_year = 2024
    end_year = 2024

    # Generate pairs of consecutive years
    if start_year==end_year:
        year_pairs=[(start_year,None)]
    else:
        year_pairs = [(start_year + i, start_year + i + 1) for i in range(end_year - start_year)]
    # Print the result
    tasks=[]
    start=20240601000000
    for domain in domains:
        for pair in year_pairs:
            print('add dom')
            task = asyncio.create_task(one(domain,pair[0],pair[1]))
            tasks.append(task)

    await asyncio.gather(*tasks)
    print(f"Time taken for asynchronous execution with concurrency limited by semaphore: {time.time() - start_time} seconds")
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
    
    asyncio.run(main())import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
import json,os
from DataRecorder import Recorder
import csv
import asyncio
proxy_url=None
domain='toolify.ai'
domain='claude.site'
domain='revved.com'
domain='https://www.amazon.com/sp?ie=UTF8&seller='
domain='https://www.amazon.com/sp?'
domain='https://www.amazon.com/sp?_encoding=UTF8&marketplaceID=ATVPDKIKX0DER&orderID=&seller='
domain='https://www.amazon.com/sp?_encoding=UTF8&marketplaceID='
domain='youtube.com'
domains=['https://www.tiktok.com/tag']
domains=['https://www.tiktok.com/@']

# domain='https://www.amazon.com/s'
# domain='https://www.amazon.com/sp?ie=UTF8&seller='

#google search  
#site:tiktok.com/tag/

# site:tiktok.com/tag/ after:2024-07-01 before:2024-08-01
def process_line(csv_file,lines):
    fieldnames = ['timestamp', 'url']

    file_exists = os.path.isfile(csv_file)
    if not file_exists:

        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    for line in lines:
        try:
            if ' ' in line:
                line=str(line).strip()
                parts = line.split(' ')
                timestamp, original_url = parts[0], parts[1]
                    
                data={'timestamp':timestamp,'url':original_url}
                with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    # if not file_exists:
                        # writer.writeheader()
                    writer.writerow(data)
        except:
            print('failed to save',line)
async def geturls(domain,start,end):
    no_subs=None
    subs_wildcard = "*." if not no_subs else ""
    # subs_wildcard=''
    domainname = domain.replace("https://", "")
    domainname=domainname.split('/')[0]
    csv_file=f'result/waybackmachines-{domainname}-user.csv'
    outfile=Recorder(f'waybackmachines-{domainname}.csv')

    query_url = f"http://web.archive.org/cdx/search/cdx?url={subs_wildcard}{domain}/&fl=timestamp,original,mimetype,statuscode,digest"
    query_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&fl=timestamp,original"
    # fileter='&statuscode=200'
    filter="&collapse=digest"
    filter="&collapse=urlkey"
    fileter=None
    if not end: 
        fileter=f'&statuscode=200&from={start}'
    else:
        fileter=f'&statuscode=200&from={start}&to={end}'

    filter="&collapse=urlkey"+fileter
    query_url=query_url+filter

    # query_url=query_url+'&matchType=prefix'
    # query_url=query_url+'&from=2024&to=2024'

    # For example: http://web.archive.org/cdx/search/cdx?url=archive.org&from=2010&to=2011



    # query_url='https://web.archive.org/__wb/sparkline?output=json&url=toolify.ai&collection=web'
    # connector = ProxyConnector.from_url(proxy_url)
    headers = {'Referer': 'https://web.archive.org/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/92.0.4515.107 Safari/537.36'}
    # initialize an AIOHTTP client with the SOCKS proxy connector
    print('start to query',query_url)
    try:
        async with aiohttp.ClientSession(connector=None) as session:
            async with session.get(query_url,
                                   headers=headers,
                                   # proxy='http://127.0.0.1:1080',
                                   timeout=300000) as resp:
                print(resp.status, query_url)
                if resp.status != 200:
                    print(f"Received status code {resp.status}.")
                    return

                count = 0
                buffer = bytearray()  # Buffer to store partial read data
                while True:
                    chunk = await resp.content.read(1024)  # Read 1024 bytes chunk
                    if not chunk:
                        # No more data, process remaining buffer
                        if buffer:
                            process_line(csv_file, [buffer.decode('utf-8', 'replace')])
                        break
                    
                    buffer.extend(chunk)  # Append new data to buffer
                    
                    # Process complete lines in the buffer
                    raw = buffer.decode('utf-8', 'replace')
                    lines = raw.splitlines(True)
                    for line in lines[:-1]:  # Process all complete lines
                        process_line(csv_file, [line])
                    
                    buffer = bytearray(lines[-1], 'utf-8')  # Keep the last potentially incomplete line
                    
                    # Example: Print progress
                    count += len(lines)
                    print(f"Processed {count} lines so far...")
    
    except aiohttp.ClientError as e:
        print(f"Connection error: {e}")
        print('start to query',query_url)

    except Exception as e:
        print(f"Error fetching data: {e}")
            # out.append(Wurl(urls[1], urls[2]))
        # return out
        # return out
        print('start to query',query_url)

        outfile.record()
import time
start_time = time.time()
async def one(domain,start,end):
    retries = 5
    for i in range(retries):
        try:

            await geturls(domain,start,end)
            break  # 如果成功，则退出循环
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"{start}-{end} Connection error on attempt {i+1}: {e}")
            
            if i < retries - 1:
                await asyncio.sleep(20*i*(i+1))  # 指数退避策略
            else:
                print("Max retries reached. Exiting.")
                return
async def main():

    # Start and end years
    start_year = 2024
    end_year = 2024

    # Generate pairs of consecutive years
    if start_year==end_year:
        year_pairs=[(start_year,None)]
    else:
        year_pairs = [(start_year + i, start_year + i + 1) for i in range(end_year - start_year)]
    # Print the result
    tasks=[]
    start=20240601000000
    for domain in domains:
        for pair in year_pairs:
            print('add dom')
            task = asyncio.create_task(one(domain,pair[0],pair[1]))
            tasks.append(task)

    await asyncio.gather(*tasks)
    print(f"Time taken for asynchronous execution with concurrency limited by semaphore: {time.time() - start_time} seconds")
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
    
    asyncio.run(main())
