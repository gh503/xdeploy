# Ubuntu 20.04 Linux 开发环境一键部署

部署涉及以下3个大部分，分别是：
- 1.基础包安装
- 2.Shell环境
- 3.Vim环境

## 1.基础包安装

Ubuntu20.04基础开发包，常用工具安装，如curl,wget等。

## 2.Shell环境

安装并设置login shell: zsh。对bash和zsh使用公共和单独配置。
.shell目录为公共配置，包括一些alias、环境变量、配置文件加载等。
tmux作为单独配置存在，便于单窗口开多个shell操作。
git shell同时配置，并包括常用的推荐优化配置。

其中需要设置git

## 3.Vim环境

Vim作为基础编辑器使用。主要使用coc.nvim插件，多个扩展一键安装，非常好使。

同时安装python2,python3。并将python3作为默认python解释器。
ruby、tcl、java、nodejs等工具，并进行了优化配置。

## 说明

详细使用，需要参考配置。Ubuntu开机即用。其他发行版应该也支持，仅在20.04LTS上使用过。
