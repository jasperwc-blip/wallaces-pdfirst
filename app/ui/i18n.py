from __future__ import annotations


TRANSLATIONS = {
    "en": {
        "app_title": "Wallace's PDFirst",
        "image_pdf": "Image to PDF",
        "transcript": "Transcript to Word/PDF",
        "merge": "Merge PDF",
        "split": "Split PDF",
        "rotate": "Rotate PDF",
        "pdf_word": "PDF to Word/PPT",
        "watermark": "Add Watermark",
        "settings": "Settings",
        "about": "About",
        "output": "Output",
        "run": "Run",
        "browse": "Browse",
        "log": "Status Log",
        "drop": "Drop files here or click Add Files",
        "language": "Language",
        "save_settings": "Save Settings",
        "settings_saved": "Settings kept for this session.",
        "settings_note": "Choose the display language for the app. Document processing remains local by default.",
    },
    "zh_Hans": {
        "app_title": "Wallace's PDFirst",
        "image_pdf": "图片转 PDF",
        "transcript": "字幕稿转 Word/PDF",
        "merge": "合并 PDF",
        "split": "拆分 PDF",
        "rotate": "旋转 PDF",
        "pdf_word": "PDF 转 Word/PPT",
        "watermark": "添加水印",
        "settings": "设置",
        "about": "关于",
        "output": "输出",
        "run": "运行",
        "browse": "浏览",
        "log": "状态日志",
        "drop": "将文件拖放到这里，或点击添加文件",
        "language": "语言",
        "save_settings": "保存设置",
        "settings_saved": "本次会话的设置已保存。",
        "settings_note": "选择应用程序显示语言。文档处理默认在本机进行。",
    },
    "zh_Hant": {
        "app_title": "Wallace's PDFirst",
        "image_pdf": "圖片轉 PDF",
        "transcript": "逐字稿轉 Word/PDF",
        "merge": "合併 PDF",
        "split": "分割 PDF",
        "rotate": "旋轉 PDF",
        "pdf_word": "PDF 轉 Word/PPT",
        "watermark": "加入浮水印",
        "settings": "設定",
        "about": "關於",
        "output": "輸出",
        "run": "執行",
        "browse": "瀏覽",
        "log": "狀態記錄",
        "drop": "將檔案拖放到這裡，或按加入檔案",
        "language": "語言",
        "save_settings": "儲存設定",
        "settings_saved": "本次工作階段的設定已保留。",
        "settings_note": "選擇應用程式顯示語言。文件處理預設在本機進行。",
    },
}


class Translator:
    def __init__(self, language: str = "en") -> None:
        self.language = language

    def t(self, key: str) -> str:
        return TRANSLATIONS.get(self.language, TRANSLATIONS["en"]).get(key, key)
