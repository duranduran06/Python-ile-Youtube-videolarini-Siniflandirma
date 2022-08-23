from youtubesearchpython import Transcript
from youtubesearchpython import VideosSearch
from youtubesearchpython import *
from youtube_transcript_api import YouTubeTranscriptApi
import os


def searchVideo(category,limit):
	index = 0
	videos = []
	search = CustomSearch(category,searchPreferences="EgIoAQ")

	#search = CustomSearch(category,searchPreferences="EgIoAQ253D253D")
	while index<limit:
		results = search.result()
		for video in results['result']:
			index+=1
			info = video['title'] + "," + video['id']
			#videos.append(video['id'])			
			videos.append(info)			
		search.next()
	

	return videos


def searchSubtitle(videoInfo):
	

	videoId = videoInfo.split(",")[1]
	videoTitle = videoInfo.split(",")[0]

	text = []	
	
	try:
		transcript_list = YouTubeTranscriptApi.list_transcripts(videoId)
		transcript = transcript_list.find_generated_transcript(['en'])
		#transcript = transcript_list.find_manually_created_transcript(['en'])
		
		subtitle = transcript.fetch()
		text.append(videoTitle)
		tempStr = ""
		for i in subtitle:
			temp = i['text']
			if temp!="[Music]":
				tempStr += temp

		text.append(tempStr)
		return text
	except:
		return -1


def saveSubtitle(videoSub,category):
  
	forbidden = ["<",">",":",'"',"/","\\","|","?","*"] # windows dosya adları bu karakterleri içeremez
	files = os.listdir()
	if category not in files:
		os.mkdir(category)
		os.chdir(category)
	else:
		os.chdir(category)
	temp = ""
	videoName = videoSub[0]

	for i in videoName:
		if i not in forbidden:
			temp+=i
	videoName = temp

	file = open(videoName+".txt","w",encoding="utf-8")
	file.write(videoSub[1])
	file.close()
	os.chdir("../")

def esitYap():
  os.chdir("/content/altyazi")
  dirlist = [filename for filename in os.listdir() if os.path.isdir(filename)]
  videoSayilar = []
  for i in dirlist:
    os.chdir(i)
    sayi = len(os.listdir())
    videoSayilar.append(sayi)
    os.chdir("../")
    
  minSayi = min(videoSayilar)  
  for i in dirlist:
    os.chdir(i)
    files = os.listdir()
    for i in range(len(files)):
      if i>minSayi:
        os.remove(files[i])
    os.chdir("../")




cat = ["science","child educational","technology news","literature","blockchain","health","biology","artificial intelligence","economy","math","sport"]



for j in cat:


	print("şu anda "+j+" çalışıyor")
	arr = searchVideo(j,500)


	for i in arr:
		subtitle = searchSubtitle(i)
		if subtitle!=-1:
			saveSubtitle(subtitle,j)