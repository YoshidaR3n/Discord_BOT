
import discord
from discord.ext import commands
from pathlib import Path

#独自.pyファイル
import config
from open_ai_api import get_response
from get_youtube_url import get_youtube_url
from create_voice import create_voice

#BOTトークン
TOKEN = config.BOT_TOKEN

# グローバル変数としてvoice_clientを定義
voice_client = None

#BOTに付与する権限類
intents = discord.Intents.default()
#intents.members = True # メンバー管理の権限
intents.message_content = True # メッセージの内容を取得する権限

# Botをインスタンス化
bot = commands.Bot(
    command_prefix="!", # !でコマンドを実行
    case_insensitive=True, # コマンドの大文字小文字を区別しない
    intents=intents # 権限を設定
)

# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("ログインしました")


# メッセージ受信時に動作する処理
@bot.command()
async def ai(ctx, *input_message):
  # メッセージ送信者がBotだった場合は無視する
    if ctx.author.bot:
        return

    if input_message:
        # メッセージの返信
        response = get_response(input_message)
        print(input_message)
        await ctx.send(response["text"])

        #話者がチャンネルにいて、voice_clientがチャンネルに接続されていることを確認
        if ctx.author.voice and voice_client is not None and voice_client.is_connected(): 
            # 音声ファイルのパスを指定
            audio_source = discord.FFmpegPCMAudio(f"{Path(__file__).parent}/tmp_file/res_voice.wav")
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=lambda e: print("再生終了:", e))
   
    else:
      await ctx.send("コマンドに続けて質問したいことを教えてね！")

# ボイスチャンネルに参加し、音声ファイルを再生するコマンド
@bot.command()
async def join(ctx):
    global voice_client #global変数のvoice_clientを指定、そうしないとaiコマンドで呼び出せない

    # ボイスチャンネルにユーザーがいるか確認
    if ctx.author.voice is None:
        await ctx.send("ボイスチャンネルに参加してください。")
        return

    # ユーザーのボイスチャンネルに接続
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

# 音声を停止し、ボイスチャンネルから切断するコマンド
@bot.command()
async def stop(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("ボイスチャンネルから切断したのだ")
    else:
        await ctx.send("ボイスチャンネルに接続していないのだ")

@bot.command()
async def play(ctx, url):
    play_url = get_youtube_url(url)

    # 音声ソースを作成
    audio_source = discord.FFmpegPCMAudio(play_url)
    audio_source = discord.PCMVolumeTransformer(audio_source, volume=0.5)

    #話者がチャンネルにいて、voice_clientがチャンネルに接続されていることを確認
    if ctx.author.voice and voice_client is not None and voice_client.is_connected(): 
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=lambda e: print("再生終了:", e))

# @bot.event
# async def on_message(message: discord.Message):
#     """メッセージをおうむ返しにする処理"""

#     if message.author.bot: # ボットのメッセージは無視
#         return

# #話者がチャンネルにいて、voice_clientがチャンネルに接続されていることを確認
#     if message.author.voice and voice_client is not None and voice_client.is_connected(): 
#         # 音声ファイルのパスを指定
#         create_voice(message)
#         audio_source = discord.FFmpegPCMAudio(f"{Path(__file__).parent}/tmp_file/res_voice.wav")
#         if not voice_client.is_playing():
#             voice_client.play(audio_source, after=lambda e: print("再生終了:", e))

# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)