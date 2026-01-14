import os, time
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import mimetypes
import uuid
from pathlib import Path
import html
import re


load_dotenv()

sb = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

st.set_page_config(page_title="生日祝福墙Happy Birthday", page_icon="🎂", layout="wide")
st.markdown("""
<div class="card">
  <div style="font-size:28px; font-weight:800;">🎂 生日祝福墙</div>
  <div style="margin-top:6px; opacity:.9; line-height:1.6;">
    这里装着一些人想对你说的话。<br/>
    愿你被温柔记得，愿你一直快乐。
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")

st.title("🎂 25岁生日快乐——田圳宇")

st.markdown("""
<style>
:root{
  --pinkA:#ffe6ef;
  --pinkB:#ffd1e3;
  --pinkC:#ffb3d1;
  --pinkStrong:#ff5fa2;

  --card:#ffffffcc;
  --cardBorder:#ffb3d155;
  --text:#2b2b33;
  --muted:#6b6b78;
}

/* 顶部 UI 隐藏 */
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
#MainMenu, footer{
  visibility: hidden !important;
  height: 0 !important;
}

/* 全局浅粉背景（亮粉风） */
.stApp{
  background:
    radial-gradient(900px 500px at 15% 10%, var(--pinkB), transparent 60%),
    radial-gradient(800px 500px at 85% 20%, var(--pinkC), transparent 55%),
    radial-gradient(1000px 700px at 40% 90%, #ffd9ea, transparent 60%),
    linear-gradient(180deg, var(--pinkA), #fff7fb);
  color: var(--text) !important;
}

.block-container{
  max-width: 1100px;
  padding-top: 2.0rem;
  padding-bottom: 3rem;
}

/* Tabs */
.stTabs [data-baseweb="tab"]{
  border-radius: 14px;
  padding: 10px 16px;
  color: var(--text) !important;
}
.stTabs [aria-selected="true"]{
  background: #ffffffaa !important;
  border: 1px solid var(--cardBorder) !important;
}

/* 输入框白底黑字 */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea{
  background: #fff !important;
  color: #111 !important;
  border: 1px solid rgba(0,0,0,0.10) !important;
  border-radius: 14px !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder{
  color: rgba(0,0,0,0.40) !important;
}

/* File uploader */
section[data-testid="stFileUploaderDropzone"]{
  background: #ffffffaa !important;
  border: 1px dashed var(--cardBorder) !important;
  border-radius: 16px !important;
}
section[data-testid="stFileUploaderDropzone"] *{
  color: var(--muted) !important;
}
section[data-testid="stFileUploaderDropzone"] button{
  background: #fff !important;
  color: #111 !important;
  border: 1px solid rgba(0,0,0,0.12) !important;
  border-radius: 12px !important;
  font-weight: 800 !important;
}

/* 按钮 */
.stButton button{
  background: linear-gradient(135deg, #ffb3d1, #ff5fa2) !important;
  color: #fff !important;
  border-radius: 16px !important;
  font-weight: 900 !important;
  padding: .7rem 1.2rem !important;
  border: 0 !important;
}

/* 卡片 */
.card{
  background: var(--card) !important;
  border: 1px solid var(--cardBorder) !important;
  border-radius: 22px;
  padding: 16px;
  box-shadow: 0 18px 60px rgba(255,95,162,.12);
  backdrop-filter: blur(10px);
}
.mini{
  color: var(--muted);
  font-size: 12px;
}

/* 卡片内媒体 */
.media{
  margin-top: 12px;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--cardBorder);
  background: #fff;
}
.media img, .media video{
  width: 100%;
  display: block;
}
.filelink{
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 14px;
  background: #fff;
  border: 1px solid var(--cardBorder);
}
.filelink a{ color: #222; text-decoration: none; }
.filelink a:hover{ text-decoration: underline; }


/* ===== 横向滑动相册（媒体横向滚动） ===== */
.media-wrap {
  margin-top: 14px;
  display: flex;              /* 由 grid 改成横向 flex */
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 8px;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

/* 滚动条稍微好看一点（可删） */
.media-wrap::-webkit-scrollbar { height: 8px; }
.media-wrap::-webkit-scrollbar-thumb {
  background: rgba(255,105,180,0.35);
  border-radius: 999px;
}
.media-wrap::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.5);
  border-radius: 999px;
}

/* 单个媒体卡片：固定宽度，横向排列 */
.media-item {
  flex: 0 0 78%;             /* 一屏显示 1 张为主，旁边露一点下一张 */
  max-width: 420px;          /* 电脑端不会太宽 */
  scroll-snap-align: start;
  overflow: hidden;
  border-radius: 16px;
  background: rgba(255, 240, 245, 0.65);
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid rgba(255,182,193,0.35);
}

/* 图片/视频尺寸限制（关键） */
.media-item img,
.media-item video {
  width: 100%;
  height: 320px;             /* 固定高度更像相册 */
  object-fit: contain;       /* 不裁脸，不拉伸 */
  display: block;
  background: #fff;
}

/* 手机更小一点 */
@media (max-width: 768px) {
  .media-item { flex-basis: 88%; }
  .media-item img, .media-item video { height: 260px; }
}

/* 文件链接也当一个“滑动卡片” */
.media-item.file {
  padding: 14px;
  font-size: 14px;
  background: rgba(255, 220, 235, 0.65);
}
.media-item.file a { color:#222; text-decoration:none; }
.media-item.file a:hover { text-decoration:underline; }

/* 视频底色 */
.media-item video {
  background: #000;
}

/* 文件下载块 */
.media-item.file {
  padding: 10px 14px;
  font-size: 14px;
  background: rgba(255, 220, 235, 0.65);
  border-radius: 12px;
}
            
            /* 卡片头部：防止名字被时间挤没/覆盖 */
.card-head{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:12px;
}

.card-name{
  font-weight:900;
  font-size:16px;
  max-width:70%;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}

.card-time{
  font-size:12px;
  color: var(--muted);
  white-space:nowrap;
  flex: 0 0 auto;
}
</style>
""", unsafe_allow_html=True)


tab1, tab2= st.tabs(["✍️ 上传祝福 Upload a Message", "🧡 查看祝福墙 View the Message Wall"])

with tab1:
    st.caption("💗 每一条祝福都会被珍藏，请留下你的名字/ Every message matters. Please leave your name.")
    name = st.text_input("署名（必填） / Name (required)")
    msg = st.text_area("祝福语（必填） / Your message (required)", height=160)
    st.caption("💗 可以上传任何你觉得可以表达心意的图片，视频和文件也可以/ Can upload anything that you wish to express, pictures, videos or files")
    files = st.file_uploader(
        "上传图片 / 视频 / 文件（可上传多个） / Upload photos, videos or files (optional)",
        type=["png","jpg","jpeg","webp","gif","mp4","mov","webm","m4v","pdf"],
        accept_multiple_files=True
    )
    if st.button("提交祝福 / Submit"):
            if not name.strip():
                st.error("请留下你的署名 / Please enter your name")
            elif not msg.strip():
                st.error("祝福语不能为空 / Message cannot be empty")
            else:
                urls = []
                metas = []

                if files:
                    for f in files:
                        suffix = Path(f.name).suffix.lower()
                        path = f"{int(time.time()*1000)}_{uuid.uuid4().hex}{suffix}"

                        content_type = f.type or mimetypes.guess_type(f.name)[0] or "application/octet-stream"

                        sb.storage.from_("bday-media").upload(
                            path,
                            f.getvalue(),
                            {"content-type": content_type}
                        )

                        url = sb.storage.from_("bday-media").get_public_url(path)
                        urls.append(url)
                        metas.append({"name": f.name, "type": content_type})

                sb.table("messages").insert({
                    "name": name.strip(),
                    "message": msg,
                    "media_urls": urls,
                    "media_meta": metas
                }).execute()

                st.success("提交成功！去祝福墙看看～ / Submitted successfully! Go check the messages ✨")

def media_blocks(urls, metas):
    if not urls:
        return ""

    html_str = '<div class="media-wrap">'

    for i, url in enumerate(urls):
        meta = metas[i] if i < len(metas) else {}
        t = meta.get("type", "")
        name = html.escape(meta.get("name", "file"))  # ✅ 现在能正常用了

        if t.startswith("image/"):
            html_str += f'''
            <div class="media-item">
              <img src="{url}" loading="lazy" />
            </div>
            '''
        elif t.startswith("video/"):
            html_str += f'''
            <div class="media-item">
              <video controls playsinline preload="metadata">
                <source src="{url}" type="{t}">
              </video>
            </div>
            '''
        else:
            html_str += f'''
            <div class="media-item file">
              📎 <a href="{url}" target="_blank">{name}</a>
            </div>
            '''

    html_str += '</div>'
    return html_str


def clean_legacy_msg(s: str) -> str:
    if not s:
        return ""
    # 把你之前不小心拼进去的提示/HTML片段尽量剔除（按你实际出现的内容再加规则）
    s = re.sub(r'hint\s*=\s*""".*?"""', "", s, flags=re.S)
    s = re.sub(r"<div.*?>.*?</div>", "", s, flags=re.S)  # 粗暴删掉 div 块（只针对旧数据救火）
    return s.strip()

with tab2:
    data = sb.table("messages") \
        .select("*") \
        .order("created_at", desc=True) \
        .execute().data

    cols = st.columns(3)
    for i, m in enumerate(data):
        with cols[i % 3]:
            raw_name = (m.get("name") or "").strip()
            raw_msg  = (m.get("message") or "").strip()

            # 空名兜底
            display_name = raw_name if raw_name else "匿名"

            created = (m.get("created_at") or "")[:19].replace("T", " ")

            urls = m.get("media_urls") or []
            metas = m.get("media_meta") or []

            # ✅ 防止用户输入 HTML 把卡片结构“插穿”
            safe_name = html.escape(display_name)
            safe_msg  = html.escape(raw_msg).replace("\n", "<br/>")

            hint = '<div class="mini">左右滑动查看更多 →</div>' if len(urls) > 1 else ""
            media_html = media_blocks(urls, metas)

            st.markdown(f"""
            <div class="card">
              <div class="card-head">
                <div class="card-name">{safe_name}</div>
                <div class="card-time">{created}</div>
              </div>

              <div style="margin-top:10px; line-height:1.65;">
                {safe_msg}
              </div>

              {hint}
              {media_html}
            </div>
            """, unsafe_allow_html=True)
