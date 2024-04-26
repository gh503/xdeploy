@echo off

@prompt %USERNAME%@%COMPUTERNAME% $P$_$C$T$F $$ 

@doskey rm=del $*
@doskey touch=copy /b NUL $*
@doskey e="%EDITOR%" $*
@doskey cat=type $*
@doskey ls=dir /D $*
@doskey sl=dir /D $*
@doskey ll=dir /P /O:G $*
@doskey cd-=popd
@doskey ..=cd ..
@doskey ...=cd ..\..
@doskey ....=cd ..\..\..
@doskey .....=cd ..\..\..\..
@doskey pwd=cd
@doskey mv=move $*
@doskey chen=chcp 437
@doskey chzh=chcp 936
@doskey chcn=chcp 65001
