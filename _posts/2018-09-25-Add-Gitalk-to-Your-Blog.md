---
layout:     post
title:      Add Gitalk to Your Blog
subtitle:   Gitalk is a comment plugin supports Markdown based on GitHub Issue
date:       2018-09-25
author:     SL
header-img: img/post-bg-keyboard.jpg
catalog: true
tags:
    - Blog
---


## Introduction

Except **Disqus**, there is also an amazing comment plugin. 
[Gitalk](https://github.com/gitalk/gitalk) is a modern comment component based on GitHub Issue and Preact.
Gitalk uses your GitHub account to log in and it supports `MarkDown`.

## Features
- Authentication with github account
- Serverless, all comments will be stored as github issues
- Both personal and organization github projects can be used to store comments
- Localization, support multiple languages [en, zh-CN, zh-TW, es-ES, fr, ru]
- Facebook-like distraction free mode (Can be enabled via the distractionFreeMode option)
- Hotkey submit comment (cmd|ctrl + enter)

## Install
Two ways.

### links
```js
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.css">
  <script src="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.min.js"></script>

  <!-- or -->

  <link rel="stylesheet" href="https://unpkg.com/gitalk/dist/gitalk.css">
  <script src="https://unpkg.com/gitalk/dist/gitalk.min.js"></script>
```
  
### npm install

    npm i --save gitalk
    
```java
import 'gitalk/dist/gitalk.css'
import Gitalk from 'gitalk'
```

### Integration with Gitalk


```js
<!-- Gitalk start  -->
{% if site.gitalk.enable %}
<!-- Link Gitalk 的支持文件  -->
<link rel="stylesheet" href="https://unpkg.com/gitalk/dist/gitalk.css">
<script src="https://unpkg.com/gitalk@latest/dist/gitalk.min.js"></script>

<div id="gitalk-container"></div>
    <script type="text/javascript">
    var gitalk = new Gitalk({

        // gitalk's main params
		clientID: `Github Application clientID`,
		clientSecret: `Github Application clientSecret`,
		repo: `your repo-name`,
		owner: 'Github username',
		admin: ['Github username'],
		id: 'identifier for a page，gitalk will create issues with this id',
    
    });
    gitalk.render('gitalk-container');
</script>
{% endif %}
<!-- Gitalk end -->
```


### Create Github Application

First we need to create a **Github Application**，[click here](https://github
.com/settings/applications/new).

And fill in the form(you can use your custom domain instead of xx.github.io)：

![Register Application](https://stuartlau.github.io/img/in-post/register-application.jpg)

Then click **Register application**.

### Configuration reposiroty
You have to enable Issue in your repository's setting, because Gitalk is based on GitHub Issue.
![GitHub Issue](https://stuartlau.github.io/img/in-post/github-issue.jpg)

### Configuration _config.xml

Get `Client ID` and `Client Secret` to fill in _config.xml related to Gitalk

```xml
  # Gitalk
  gitalk:
  enable: true    #enable or not
  clientID:     xxxx                        #your clientID
  clientSecret:  xxxx   #your clientSecret
  repo: your-repo.github.io    #repository name
  owner: your-github-account    #github username
  admin: your-github-account
  distractionFreeMode: true 

```

When all settings are done and push to your GitHub repo, wait for 
a while refresh your page and you can see Gitalk is in effect.

But there is still something we need to do or you may get the following
![Issues Not Found](https://stuartlau.github.io/img/in-post/issues-not-found.jpg)
Link your repository to Gitalk.
![Link Repository Oauth](https://stuartlau.github.io/img/in-post/link-repository-oauth.jpg)

Refresh your pages and you will see Gitalk plugin is in effect.
![Empty Comment](https://stuartlau.github.io/img/in-post/empty-comment.jpg)
You can sort the comment by time.
![Empty Comment with Menu](https://stuartlau.github.io/img/in-post/empty-comment-with-menu.jpg)