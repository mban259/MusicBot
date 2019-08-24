from discord.ext import commands
import reaction


class myHelpCommand(commands.MinimalHelpCommand):
    def init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        ctx: commands.Context = self.context
        try:
            await reaction.send_processing(ctx)
            await ctx.send("```asciidoc\n"
                           "ping: ぴんぽん\n"
                           "join: VoiceChannelに入るよ!\n"
                           "start \"filename\": filenameを再生するよ!\n"
                           "stop: 止めるよ!\n"
                           "pause: 一時停止するよ!\n"
                           "resume: 再開するよ!\n"
                           "leave: VoiceChannelから出るよ!\n"
                           "list: ファイルを表示するよ!\n"
                           "delete \"filename\": filenameを削除するよ!\n"
                           "help: へるぷ!\n"
                           "DMにファイルを貼ればアップロードできるよ!\n"
                           "\"コメントを追加\"でファイル名指定ができるよ!\n"
                           "```")
            await reaction.send_done(ctx)
        except:
            await reaction.send_error(ctx)



