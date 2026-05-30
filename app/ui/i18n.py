from __future__ import annotations


TRANSLATIONS = {
    "en": {
        "app_title": "Wallace's PDFirst",
        "image_pdf": "Image to PDF",
        "transcript": "Transcript to Word/PDF",
        "merge": "Merge PDF",
        "split": "Split PDF",
        "rotate": "Rotate PDF",
        "watermark": "Add Watermark",
        "settings": "Settings",
        "about": "About",
        "output": "Output",
        "run": "Run",
        "browse": "Browse",
        "log": "Status Log",
        "drop": "Drop files here or click Add Files",
    },
    "zh_Hant": {
        "app_title": "Wallace's PDFirst",
        "image_pdf": "圖片轉 PDF",
        "transcript": "逐字稿轉 Word/PDF",
        "merge": "合併 PDF",
        "split": "分割 PDF",
        "rotate": "旋轉 PDF",
        "watermark": "加入浮水印",
        "settings": "設定",
        "about": "關於",
        "output": "輸出",
        "run": "執行",
        "browse": "瀏覽",
        "log": "狀態記錄",
        "drop": "拖放檔案到這裡，或按加入檔案",
    },
    "zh_Hans": {
        "app_title": "Wallace's PDFirst",
        "image_pdf": "图片转 PDF",
        "transcript": "转写稿转 Word/PDF",
        "merge": "合并 PDF",
        "split": "拆分 PDF",
        "rotate": "旋转 PDF",
        "watermark": "添加水印",
        "settings": "设置",
        "about": "关于",
        "output": "输出",
        "run": "运行",
        "browse": "浏览",
        "log": "状态日志",
        "drop": "拖放文件到这里，或点击添加文件",
    },
}


class Translator:
    def __init__(self, language: str = "en") -> None:
        self.language = language

    def t(self, key: str) -> str:
        return TRANSLATIONS.get(self.language, TRANSLATIONS["en"]).get(key, key)
