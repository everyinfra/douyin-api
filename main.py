"""抖音 API 示例（Douyin API in Python）。

  python main.py search 露营装备 --out videos.csv         # 按关键词搜视频 / search videos
  python main.py video "<视频链接>" --out video.json      # 视频详情 / video detail
  python main.py comments "<视频链接>" --out comments.csv # 视频评论 / comments
  python main.py user <user_id>                           # 作者主页 / creator profile
  python main.py posts <user_id> --out posts.csv          # 作者的作品 / a creator's videos
"""
import argparse

from everyinfra import fetch, report

SORTS = ["relevance", "newest", "most_liked"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜视频 / search videos by keyword")
    s.add_argument("keyword")
    s.add_argument("--sort", choices=SORTS, help="排序 / sort order")
    v = sub.add_parser("video", help="视频详情 / one video")
    v.add_argument("url")
    c = sub.add_parser("comments", help="视频评论 / comments of one video")
    c.add_argument("url")
    u = sub.add_parser("user", help="作者主页 / creator profile")
    u.add_argument("user_id")
    po = sub.add_parser("posts", help="作者发布的作品 / a creator's videos")
    po.add_argument("user_id")
    for x in (s, v, c, u, po):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "video":
        rows, charged = fetch("video", {"url": a.url})
    elif a.cmd == "comments":
        rows, charged = fetch("comments", {"url": a.url})
    elif a.cmd == "user":
        rows, charged = fetch("profile", {"user_id": a.user_id})
    else:
        rows, charged = fetch("user_posts", {"user_id": a.user_id})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
