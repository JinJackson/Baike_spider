# Baidu Baike spider



### 1.环境要求

`pip install -r requirements.txt`

### 2. 文件结构

Bake_spider.py 程序入口

\keyword_file 需要提取的关键词（建议按照日期+时间保存，方便备份和查找）

\result 爬取结果

+ all_crawled_info.jsonl 所有爬取的结果，字段包括

  「keyword：查找的关键词, url：爬取的链接, title：链接对应的百科词条的标题（通常与keyword一致）, content：百科内容，linked_links：百科内容中包含的其他链接」

+ crawled_keyword.jsonl 所有已爬的关键词和url，用于防止重复爬取

+ Not_found_keyword_list.txt 所有未找到关键词列表，防止重复爬取



### 3. 调用方式
详见main函数
<!-- `python Baike_spider.py file_path` -->