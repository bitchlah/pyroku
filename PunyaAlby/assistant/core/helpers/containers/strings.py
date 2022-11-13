class Strings(object):
    def close_tab_string(self):
        text = "📍Welcome to ALBY PYROBOT📍\n"
        text += "Silahkan klik Tombol dibawah untuk mengetahui fitur dan cara mengoperasikan ALBY PYROBOT\n"
        text += "\n\n• Menu Ditutup"

        return text


    def home_tab_string(self):
        text = "🏠 **Home**\n\n"
        text += "📍 **ALBY-Userbot Inline Menu** 📍"

        return text


    def plugin_tab_string(self):
        text = "📍 **ALBY-Userbot Inline Menu** 📍\n\n"
        text += f"🔖 **Plugins:** `{len(self.CMD_HELP)}`"

        return text

