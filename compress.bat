set sevenzip_path=E:\Utils\Misc\7-Zip
@rem set upx_path=E:\Utils\Misc\upx300w

%sevenzip_path%\7z.exe -aoa x library.zip -olibrary\
del library.zip

cd library\
@rem %upx_path%\upx.exe --best *.*
%sevenzip_path%\7z.exe a -tzip -mx9 ..\library.zip -r
cd..
rd library /s /q

@rem %upx_path%\upx.exe --best *.*