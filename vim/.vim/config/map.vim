let g:mapleader=" "

map S :w<CR>
map Q :q<CR>
map R :source $MYVIMRC<CR>

noremap <LEADER><CR> :nohlsearch<CR>

map <LEADER>sl :set splitright<CR>:vsplit<CR>
map <LEADER>sh :set nosplitright<CR>:vsplit<CR>
map <LEADER>sj :set splitbelow<CR>:split<CR>
map <LEADER>sk :set nosplitbelow<CR>:split<CR>
map <LEADER>h <C-w>h
map <LEADER>l <C-w>l
map <LEADER>j <C-w>j
map <LEADER>k <C-w>k
map <up> :resize +3<CR>
map <down> :resize -3<CR>
map <left> :vertical resize -3<CR>
map <right> :vertical resize +3<CR>
" 转竖直分屏
map <LEADER>sv <C-w>t<C-w>H
" 转水平分屏
map <LEADER>sh <C-w>t<C-w>K

" 新建标签
map <LEADER>te :tabe<CR>
" 下一个标签
map <LEADER>tj :+tabnext<CR>
" 上一个标签
map <LEADER>tk :-tabnext<CR>
" Tab切换下一个文件
map <TAB> :bn<CR>
" Shift+Tab切换上一个文件
map <S-TAB> :bp<CR>

" 文件浏览器
nmap <LEADER>e :NERDTreeToggle<CR>
" 拼写检查
nmap <LEADER>sc :set spell!<CR>

" 切换上个主题
nmap <LEADER>cp :PreviousColorScheme<CR>
" 切换下个主题
nmap <LEADER>cn :NextColorScheme<CR>
" Tab<->空格
nmap <LEADER>rt :%retab!<CR>
" 搜索高亮
nmap <LEADER>hl :set hlsearch!<CR>


" 全选并复制
map <C-A> ggVGY
" 选中状态下复制
vmap <C-c> "+y
" 粘贴
vmap <C-p> "+p

" 重命名
nmap <LEADER>rn <Plug>(coc-rename)
" 当前分屏最大化
nmap <leader>z :call Zoom()<CR>

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

function! Zoom ()
    " check if is the zoomed state (tabnumber > 1 && window == 1)
    if tabpagenr('$') > 1 && tabpagewinnr(tabpagenr(), '$') == 1
        let l:cur_winview = winsaveview()
        let l:cur_bufname = bufname('')
        tabclose

        " restore the view
        if l:cur_bufname == bufname('')
            call winrestview(cur_winview)
        endif
    else
        tab split
    endif
endfunction
