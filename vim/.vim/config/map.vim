let g:mapleader="\<SPACE>"

nmap <LEADER>e :NERDTreeToggle<CR>  " 文件浏览器"

nmap <TAB> :bn<CR>                  " Tab切换下一个文件
nmap <S-TAB> :bp<CR>                " Shift+Tab切换上一个文件

nmap <F8> :PreviousColorScheme<CR>     " 切换上个主题
imap <F8> <ESC> :PreviousColorScheme<CR>
nmap <F7> :NextColorScheme<CR>     " 切换下个主题
imap <F7> <ESC> :NextColorScheme<CR>
nmap <F6> :%retab!<CR>              " Tab<->空格
nmap <F5> :set hlsearch!<CR>        " 搜索高亮
nmap <F4> :set cursorcolumn!<CR>    " 列显示突出
nmap <F3> :set spell!<CR>           " 拼写检查
nmap <F2> :call ProgramRun() <CR>         " 执行脚本

map <C-A> ggVGY                     " 全选并复制
vmap <C-c> "+y                      " 选中状态下复制
vmap <C-p> "+p                      " 粘贴

" 重命名
nmap <leader>rn <Plug>(coc-rename)


" TAB 自动补全
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

" <c-space> 触发补全
if has('nvim')
  inoremap <silent><expr> <c-space> coc#refresh()
else
  inoremap <silent><expr> <c-@> coc#refresh()
endif

nnoremap <silent> K :call <SID>show_documentation()<CR>


func ProgramRun()
    if &filetype == "Python"
        execute "!time python %; while true; do sleep 1; done"
    elseif &filetype == "shell"
        execute "!time bash %; while true; do sleep 1; done"
    elseif &filetype == "Ruby"
        execute "!time ruby %; while true; do sleep 1; done"
    endif
endfunc

" 保留tab缩进功能
function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction


function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  elseif (coc#rpc#ready())
    call CocActionAsync('doHover')
  else
    execute '!' . &keywordprg . " " . expand('<cword>')
  endif
endfunction
