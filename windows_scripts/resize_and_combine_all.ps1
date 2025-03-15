# Image/gif resizer, gif-ifier, and merger.
#
# Requirements:
#	Requires ImageMagick to be installed and on your path.
#	How to install:
#	- Get https://scoop.sh/
#	- Run `scoop install imagemagick`
#
# Usage:
# 	The script prompts you for inputs when you run it.
# 	If you want to use the functions in your own scripts you can copy their lines directly.
#
# Other platforms (linux):
#	This is a powershell script, but the imagemagick commands it will work on any platform with ImageMagick installed.
#	Find the `magick` commands in the functions below, and copy them into your terminal, replacing the variables with your own values directly.
#
# What this does:
# 	This script will convert every jpg+png+webp+gif+mp4 file in the input-folder to a gif of given pixel-size. 
#	It then combines every gif in the output-folder into a single gif.
#
# 	If you want to merge your own gifs without converting anything, 
#	you can put your gifs directly into the output folder of this script, so the script combines them. 
#	If the folder doesn't exist you can run this script or make it manually. 
#
#	You don't need to put any images in your input folder for this.

$outFolderName = "gif_output"
$outGifName = "_combined"


Function MassForceResize {
	param (
		[string]$InDirPath,
		[string]$OutDirPath,
		[string]$InFiletype,
		[string]$OutFiletype,
		[int]$PixelSize
	  )
	if (-not (Test-Path $OutDirPath)) {
	  New-Item -Path $OutDirPath -ItemType Directory
	}
	Get-ChildItem "$InDirPath\" -Filter "*.$InFiletype" | 
	Foreach-Object {
	$base = $_.BaseName
	$out  = "$OutDirPath\$base.$OutFiletype"

	#____ The ImageMagick command ____#
	#| If you're not on Windows, you can copy this line and input your own values, and it'll work on any platform that can use ImageMagick.
	magick $_.FullName -resize "${PixelSize}x${PixelSize}^" -gravity center -extent "${PixelSize}x${PixelSize}" $out

	Write-Output "Created file: $out"
	}
}



Function MergeGifs {
	param (
	[string]$InDirPath,
	[string]$OutFileName,
	[float]$DelayInSeconds
	)
	$DelayInCentiSeconds = $DelayInSeconds*100
	$inp = "$InDirPath\*.gif" 
	$out = "$InDirPath\$OutFileName.gif"
	if (Test-Path $out) {
		Remove-Item $out
	}

	#____ The ImageMagick command ____#
	#| If you're not on Windows, you can copy this line and input your own values, and it'll work on any platform that can use ImageMagick.
	magick -delay $DelayInCentiSeconds $inp $out

	Write-Output "Created file: $out"
}




$inPath = ""
$answer = Read-Host "Enter path of folder to convert ('.' for current path)"
if ($answer -eq '.') {
	$inPath = $PSScriptRoot
} else {
	$inPath = $answer
}
$outPath = "$inPath\$outFolderName"
Write-Host "Using input-folder path:  $inPath"
Write-Host "Using output-folder path: $outPath"

Write-Host "`n## INFORMATION ##"
Write-Host "`n### What this does ###"
Write-Host "This script will convert every jpg+png+webp image in the input-folder to a gif of given pixel-size. It then combines every gif in the output-folder `"$outFolderName`", into a single gif named `"$outGifName`"."
Write-Host "`n### How to combine your own gifs ###"
Write-Host "If you only want to merge gifs, you can put your gifs directly into the output folder of this script, so the script combines them. If the folder doesn't exist you can run this script or make it manually. You also don't need to put images in your input folder."


Write-Host "`n## IMAGE CONVERTING ##"
$targetsize = 0.0
do {
	$inp = Read-Host "Enter pixel size to make output gifs (e.g. 32 or 16)"
	$inputValid = [int]::TryParse($inp, [ref]$targetsize)
	if (-not $inputValid) {
		Write-Host "Input wasn't an integer, try again: "
	}
} while (-not $inputValid)

MassForceResize -InDirPath $inPath -OutDirPath "$outPath" -InFiletype "jpg"  -OutFiletype "gif" -PixelSize $targetsize
MassForceResize -InDirPath $inPath -OutDirPath "$outPath" -InFiletype "png"  -OutFiletype "gif" -PixelSize $targetsize
MassForceResize -InDirPath $inPath -OutDirPath "$outPath" -InFiletype "webp" -OutFiletype "gif" -PixelSize $targetsize
MassForceResize -InDirPath $inPath -OutDirPath "$outPath" -InFiletype "gif"  -OutFiletype "gif" -PixelSize $targetsize
MassForceResize -InDirPath $inPath -OutDirPath "$outPath" -InFiletype "mp4"  -OutFiletype "gif" -PixelSize $targetsize


Write-Host "`n## IMAGE LOOPING ##"
$secondsBetweenGifs = 0.0
do {
	$inp = Read-Host "Enter number of seconds delay between each image, use commas for floats"
	$inputValid = [float]::TryParse($inp, [ref]$secondsBetweenGifs)
	if (-not $inputValid) {
		Write-Host "Input wasn't float, try again. You need to use commas for floats, e.g. '3,5'"
	}
} while (-not $inputValid)


MergeGifs -InDirPath "$outPath" -OutFileName "_combined" -DelayInSeconds $secondsBetweenGifs


Write-Host "Script complete"
