set sevenzip_path=E:\Utils\Misc\7-Zip
@rem set upx_path=E:\Utils\Misc\upx300w
set target=%1

%sevenzip_path%\7z.exe -aoa x "%target%.zip" -o"%target%\"
del "%target%.zip"

cd "%target%\"
@rem %upx_path%\upx.exe --best *.*
%sevenzip_path%\7z.exe a -tzip -mx9 "..\%target%.zip" -r
cd..
rd "%target%" /s /q

@rem %upx_path%\upx.exe --best *.*