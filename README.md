# 抖音 API（Douyin API）

[中文](#中文) · [English](#english)

## 中文

本仓库用 Python 或 curl 读抖音公开数据：按关键词搜视频，读视频详情和评论，查作者主页和他发布的作品。只需一把 EveryInfra API Key，不用抖音账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 5 个能力每千次 $0.56 到 $8.33，失败和空结果不收费。抖音共 50 个能力，其中 43 个现在可用：<https://everyinfra.com/douyin-api?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/douyin-api.git
cd douyin-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search 露营装备 --out videos.csv
python main.py video "<视频链接>" --out video.json
python main.py comments "<视频链接>" --out comments.csv
python main.py user <user_id>
python main.py posts <user_id> --out posts.csv
```

- 视频链接用 `search` 结果里的 `url`。
- `user` 和 `posts` 的 `user_id` 用 `search` 结果里的 `author_id`，是以 MS4w 开头的 secUid；昵称和短数字抖音号不能用。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"douyin","action":"search","params":{"keyword":"露营装备"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`video`、`comments`、`profile`、`user_posts` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server/douyin?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $8.33 |
| 视频详情 | `video` | $0.56 |
| 评论 | `comments` | $0.56 |
| 主页或对象详情 | `profile` | $0.56 |
| 用户内容 | `user_posts` | $0.56 |

- 按调用次数计费，每次约 $0.00056 到 $0.0083；失败、空结果、参数错误和鉴权失败都不收费。
- `comments` 按要的条数计费，每 20 条算一次调用，没返回数据的部分不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>
- 抖音其他 38 个可用能力的单价见平台页 <https://everyinfra.com/douyin-api?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### 返回字段

下面是这 5 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `media_type` | 媒体类型。 |
| `video_url` | 视频播放地址（带签名、会过期，要留存请及时下载）；图文笔记或来源没给时为 null。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 分享/转发数。 |
| `collect_count` | 收藏数。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_uid` | 作者（评论里是评论者）的数字用户 ID；author_id 是 secUid，两者是同一个人的两种 ID。 |
| `author_bio` | 作者主页简介（search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上）。 |
| `video_width` | 视频画面宽度（像素）。 |
| `video_height` | 视频画面高度（像素）。 |
| `author_avatar_url` | 作者头像链接：search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上是博主的，live_room 上是主播的，comments 行上是评论者的。 |
| `cover_image_url` | 封面图链接：search / user_posts / posts_batch / related_posts / mix_posts / music_posts / media_links 是作品封面，music_search / music_detail 是音乐封面，billboard_topic_hot 是话题配图，user_mixes 是合集封面，live_room 是直播间封面；带签名的会过期。 |
| `author_follower_count` | 作者粉丝数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `duration_sec` | 视频时长（秒）。 |
| `hashtags` | 正文里的话题标签数组，按出现顺序；没有时不出现这个字段。 |
| `hashtag_ids` | 作品话题 ID 列表，与 hashtags 同序一一对应（search / user_posts / video）。 |
| `search_rank` | 在这次关键词搜索结果里的名次（从 1 开始）：product_search 行是商品，search 行是作品，hashtag_search 行是话题。 |
| `duration_seconds` | 时长，单位秒。 |
| `image_urls` | 图片链接数组，按平台展示顺序；没有图片时不出现这个字段。 |

完整参数和字段：<https://everyinfra.com/douyin-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

#### `video`（视频详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `media_type` | 媒体类型。 |
| `video_url` | 视频播放地址（带签名、会过期，要留存请及时下载）；图文笔记或来源没给时为 null。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 分享/转发数。 |
| `collect_count` | 收藏数。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_douyin_id` | 作者抖音号。 |
| `author_avatar_url` | 作者头像链接：search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上是博主的，live_room 上是主播的，comments 行上是评论者的。 |
| `cover_image_url` | 封面图链接：search / user_posts / posts_batch / related_posts / mix_posts / music_posts / media_links 是作品封面，music_search / music_detail 是音乐封面，billboard_topic_hot 是话题配图，user_mixes 是合集封面，live_room 是直播间封面；带签名的会过期。 |
| `author_follower_count` | 作者粉丝数。 |
| `region` | 地区。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `author_uid` | 作者（评论里是评论者）的数字用户 ID；author_id 是 secUid，两者是同一个人的两种 ID。 |
| `author_is_verified` | 作者是否认证（search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上；live_room 上是主播是否认证；comments 行上是评论者是否认证）。 |
| `author_bio` | 作者主页简介（search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上）。 |
| `author_like_count` | 作者主页获赞总数（search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts / transcript）。 |
| `title` | 标题。 |
| `music` | 作品背景音乐：id、title（曲名）、author（演唱/作者）、is_original（是否原声）、duration_sec（秒）、cover_url、play_url（音频地址，可能会过期）；没有音乐信息时没有这个键。 |
| `is_pinned` | 是否置顶（作品行：作者主页置顶作品；trending：榜单置顶词；评论行：作者置顶的评论）。 |
| `is_ad` | 是否为广告作品。 |
| `video_tags` | 平台给作品打的内容分类标签（如「美食」「探店」）。 |
| `video_width` | 视频画面宽度（像素）。 |
| `video_height` | 视频画面高度（像素）。 |
| `video_resolution` | 视频清晰度档位原文（如 720p）。 |
| `animated_cover_url` | 动态封面链接。 |
| `hashtag_ids` | 作品话题 ID 列表，与 hashtags 同序一一对应（search / user_posts / video）。 |
| `video_bitrates` | 各清晰度播放地址：[{quality（清晰度名）, bitrate（码率，bps）, fps, is_h265（是否 H.265 编码）, width, height（像素）, url}]，来源没给的项不出现；地址带签名、会过期（见 video_url_expires_at）。 |
| `download_url` | 作品视频的下载地址（带签名、会过期）。 |
| `has_watermark` | 平台对这条作品视频文件的水印标记（true 表示带水印）。 |
| `video_url_expires_at` | 播放与下载地址的失效时间（ISO 8601，UTC）；之后要重新取。 |
| `permissions` | 作者给作品设的权限：can_comment（可评论）、can_download（可下载）、can_duet（可合拍）、can_stitch（可拼接）、can_share（可分享）、can_repost（可转发）、can_save（可保存）；只含平台给了的项。 |
| `duration_sec` | 视频时长（秒）。 |
| `hashtags` | 正文里的话题标签数组，按出现顺序；没有时不出现这个字段。 |
| `duration_seconds` | 时长，单位秒。 |

完整参数和字段：<https://everyinfra.com/douyin-api/video?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

#### `comments`（评论）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `like_count` | 点赞数。 |
| `reply_count` | 回复数，通常用于评论的子回复。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_douyin_id` | 作者抖音号。 |
| `author_avatar_url` | 作者头像链接：search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上是博主的，live_room 上是主播的，comments 行上是评论者的。 |
| `author_uid` | 作者（评论里是评论者）的数字用户 ID；author_id 是 secUid，两者是同一个人的两种 ID。 |
| `author_is_verified` | 作者是否认证（search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上；live_room 上是主播是否认证；comments 行上是评论者是否认证）。 |
| `ip_location` | IP 属地（平台强制展示，非用户填写）。 |
| `liked_by_author` | 评论是否被作者点赞。 |
| `is_pinned` | 是否置顶（作品行：作者主页置顶作品；trending：榜单置顶词；评论行：作者置顶的评论）。 |
| `is_hot` | 该评论是否带「热评」标记（comments）。 |
| `is_reply` | 是否为回复。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `video_id` | 视频 ID：comments 是评论所属的视频，post_history 是查的那条视频。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `images` | 图片链接数组，按平台展示顺序；没有图片时不出现这个字段。 |
| `sticker_url` | 评论里的表情贴纸图片链接（comments）；没有贴纸时没有这个键。 |

完整参数和字段：<https://everyinfra.com/douyin-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

#### `profile`（主页或对象详情）

| 字段 | 含义 |
|---|---|
| `user_id` | 用户在原平台的唯一 ID。 |
| `douyin_id` | 抖音号（用户自定义的可搜索 ID）。 |
| `nickname` | 昵称。 |
| `bio` | 个人简介，账号自己填写的文本。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `follower_count` | 粉丝数。 |
| `following_count` | 关注数。 |
| `like_count` | 点赞数。 |
| `video_count` | 视频数：profile、profiles_batch、user_overview、billboard_account_search 是账号的作品数，trending、billboard_rise_list、billboard_challenge_hot 是这个热点下的相关视频数。 |
| `gender` | 性别。 |
| `ip_location` | IP 属地（平台强制展示，非用户填写）。 |
| `is_verified` | 是否为平台认证账号（蓝V等）。 |
| `avatar_url` | 头像图片链接。 |
| `uid` | 数字用户 ID（profile / creator_search）；user_id 是 secUid，两者是同一账号的两种 ID。 |
| `background_image_url` | 主页背景图链接。 |
| `is_live` | 账号（profile、creator_search）或直播间（live_room）在采集时是否正在直播；属于时点状态。 |
| `age` | 账号主人年龄（profile；公开了才有）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/douyin-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

#### `user_posts`（用户内容）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `media_type` | 媒体类型。 |
| `video_url` | 视频播放地址（带签名、会过期，要留存请及时下载）；图文笔记或来源没给时为 null。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 分享/转发数。 |
| `collect_count` | 收藏数。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_avatar_url` | 作者头像链接：search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上是博主的，live_room 上是主播的，comments 行上是评论者的。 |
| `author_is_verified` | 作者是否认证（search / user_posts / video / posts_batch / related_posts / mix_posts / music_posts 行上；live_room 上是主播是否认证；comments 行上是评论者是否认证）。 |
| `cover_image_url` | 封面图链接：search / user_posts / posts_batch / related_posts / mix_posts / music_posts / media_links 是作品封面，music_search / music_detail 是音乐封面，billboard_topic_hot 是话题配图，user_mixes 是合集封面，live_room 是直播间封面；带签名的会过期。 |
| `video_width` | 视频画面宽度（像素）。 |
| `video_height` | 视频画面高度（像素）。 |
| `video_bitrates` | 各清晰度播放地址：[{quality（清晰度名）, bitrate（码率，bps）, fps, is_h265（是否 H.265 编码）, width, height（像素）, url}]，来源没给的项不出现；地址带签名、会过期（见 video_url_expires_at）。 |
| `has_watermark` | 平台对这条作品视频文件的水印标记（true 表示带水印）。 |
| `duration_sec` | 视频时长（秒）。 |
| `hashtags` | 正文里的话题标签数组，按出现顺序；没有时不出现这个字段。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `title` | 标题。 |
| `music` | 作品背景音乐：id、title（曲名）、author（演唱/作者）、is_original（是否原声）、duration_sec（秒）、cover_url、play_url（音频地址，可能会过期）；没有音乐信息时没有这个键。 |
| `is_deleted` | 作品已被删除时为 true；抖音在作品行上标了才有这个键。 |
| `is_private` | 作品仅自己可见（私密）时为 true；抖音在作品行上标了才有这个键。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `duration_seconds` | 时长，单位秒。 |

完整参数和字段：<https://everyinfra.com/douyin-api/user_posts?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### 和抖音开放平台的区别

抖音有官方开放平台，入驻要过中国内地主体或实名个人认证。按关键词搜视频要过内测和能力两道申请，只给已上线、有一定用户规模的应用，默认日均 1000 次；视频列表接口只读授权账号自己的。EveryInfra 读公开内容，用一把 API Key 调，不用向抖音申请。

出处（2026-11-21 核对）：

- <https://developer.open-douyin.com/docs/resource/zh-CN/developer/join/join-into-developer-platform>
- <https://developer.open-douyin.com/docs/resource/zh-CN/dop/ability/search-management/item-search>

### 常见问题

**调用时要不要提供抖音账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.56 起。失败、空结果、参数错误和鉴权失败都不收费；`urls` 传多个链接时每个算一次。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

**能把抖音接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server/douyin?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>。Agent 能自己搜抖音内容、读评论、查账号。

**用抖音数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到抖音的哪些数据？**

抖音有 50 个能力，其中 43 个现在可用：关键词搜索、主页或对象详情、用户内容、视频详情、评论、评论回复、热榜、视频文稿、达人搜索、达人粉丝画像、达人涨粉趋势、同类达人对比、星图达人搜索、星图达人分析、星图达人报价、星图达人榜单、商品搜索、店铺商品、商品详情、直播商品搜索、话题搜索、话题详情、热点宝视频热榜、热点宝低粉爆款榜、热点宝高完播率榜、热点宝搜索热榜、热点宝账号搜索、搜索联想词、热点宝上升热点榜、热点宝挑战热榜、热点宝话题热榜、音乐详情、批量查作品、批量查作者、作品下载链接、相关推荐作品、作品数据历史、用某段音乐的作品、链接识别、热榜历史、作者的合集、合集里的作品、直播间。每个能力的参数和返回字段见平台页 <https://everyinfra.com/douyin-api?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 5 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search 露营装备 --out videos.csv` | 2026-11-21 09:41 | 10 | $0.008333 |
| `python main.py video "<视频链接>" --out video.json` | 2026-11-21 09:42 | 1 | $0.000556 |
| `python main.py comments "<视频链接>" --out comments.csv` | 2026-11-21 09:42 | 20 | $0.000556 |
| `python main.py user <user_id>` | 2026-11-21 09:42 | 1 | $0.000556 |
| `python main.py posts <user_id> --out posts.csv` | 2026-11-21 09:42 | 23 | $0.000556 |

`video` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "7648208200076573925",
  "text": "我的露营入坑全过程 从露营小白到装备齐全，坑越来越大。你们是不是也正在入坑？\n#露营\n#露营装备 \n#露营入坑 \n#户外…",
  "media_type": "video",
  "like_count": 68086,
  "comment_count": 7465,
  "share_count": 93680,
  "collect_count": 7559,
  "region": "CN",
  "posted_at": "2026-06-06T09:13:59+00:00",
  "title": "我的露营入坑全过程",
  "is_ad": false,
  "duration_sec": 289,
  "duration_seconds": 289
}
```

## English

This repo reads public Douyin data with Python or curl. You can search videos by keyword, read video details and comments, and look up a creator's profile and posts. You need one EveryInfra API key. You do not need a Douyin account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 5 capabilities cost $0.56 to $8.33 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra Douyin API has 50 capabilities; 43 are available now. All are listed on the platform page: <https://everyinfra.com/en/douyin-api?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### Quick start

```bash
git clone https://github.com/everyinfra/douyin-api.git
cd douyin-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search 露营装备 --out videos.csv
python main.py video "<video url>" --out video.json
python main.py comments "<video url>" --out comments.csv
python main.py user <user_id>
python main.py posts <user_id> --out posts.csv
```

- Take the video link from the `url` field of a `search` result.
- For `user` and `posts`, use the `author_id` from a `search` result as `user_id`. It is a secUid that starts with MS4w. Nicknames and short numeric Douyin IDs do not work.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"douyin","action":"search","params":{"keyword":"露营装备"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `video`, `comments`, `profile`, and `user_posts` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server/douyin?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $8.33 |
| `video` | $0.56 |
| `comments` | $0.56 |
| `profile` | $0.56 |
| `user_posts` | $0.56 |

- Billing is per call, about $0.00056 to $0.0083 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- `comments` is billed by the rows you ask for: every 20 rows count as one call, and blocks that come back with no rows are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>
- Prices for the other 38 available Douyin capabilities are on the platform page: <https://everyinfra.com/en/douyin-api?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### Fields

The fields of each capability are documented on the English pages linked below.

- `search`: <https://everyinfra.com/en/douyin-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>
- `video`: <https://everyinfra.com/en/douyin-api/video?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>
- `comments`: <https://everyinfra.com/en/douyin-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>
- `profile`: <https://everyinfra.com/en/douyin-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>
- `user_posts`: <https://everyinfra.com/en/douyin-api/user_posts?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### Douyin open platform vs. this API

Douyin has an official open platform for mainland China entities and real-name individuals, who must pass identity verification. Keyword video search needs a beta application and a capability application, is open only to launched apps with an established user base, and defaults to 1,000 calls a day. The video list endpoint returns only the authorizing account's own videos. EveryInfra reads public content with one API key, without applying to Douyin.

Sources (checked 2026-11-21):

- <https://developer.open-douyin.com/docs/resource/zh-CN/developer/join/join-into-developer-platform>
- <https://developer.open-douyin.com/docs/resource/zh-CN/dop/ability/search-management/item-search>

### FAQ

**Do I need a Douyin account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.56 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. When `urls` holds several links, each link counts as one call. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

**Can I connect the Douyin API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server/douyin?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>. An agent can then search Douyin content, read comments, and look up accounts by itself.

**What legal points apply when I use Douyin data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Douyin data can I get?**

The EveryInfra Douyin API has 50 capabilities; 43 are available now:

- keyword search
- profile or object details
- user content
- video details
- comments
- comment replies
- trending list
- transcript
- creator search
- creator audience
- creator growth trend
- creator benchmark
- xingtu creator search
- xingtu creator analytics
- xingtu creator rate card
- xingtu creator rankings
- product search
- shop store products
- product details
- live product search
- hashtag search
- hashtag detail
- hot video board
- low-follower hit board
- high completion-rate board
- hot search board
- Hot Spot account search
- search suggestions
- billboard rise list
- billboard challenge hot
- billboard topic hot
- music detail
- posts in bulk
- profiles in bulk
- media download links
- related posts
- post metrics history
- posts using a track
- link recognition
- trending history
- account collections
- collection posts
- live room

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/douyin-api?utm_source=github&utm_medium=example_repo&utm_campaign=douyin-api>

### Tested

Before release, we ran the 5 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search 露营装备 --out videos.csv` | 2026-11-21 09:41 | 10 | $0.008333 |
| `python main.py video "<video url>" --out video.json` | 2026-11-21 09:42 | 1 | $0.000556 |
| `python main.py comments "<video url>" --out comments.csv` | 2026-11-21 09:42 | 20 | $0.000556 |
| `python main.py user <user_id>` | 2026-11-21 09:42 | 1 | $0.000556 |
| `python main.py posts <user_id> --out posts.csv` | 2026-11-21 09:42 | 23 | $0.000556 |

## License

MIT
