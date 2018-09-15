---
layout:     post
title:      How to Deploy Slides on Github Pages
subtitle:   Use reveal.js to make magic happen 
date:       2018-06-15
author:     SL
header-img: img/post-bg-desk.jpg
catalog: true
tags:
    - Tutorial
---

## Build from scratch

	$ git clone https://github.com/hakimel/reveal.js.git
	$ cd reveal.js
	$ rm -RF.git
	$ git remote add origin git@github.com:yourname/repo-name.git
	$ git add .
	$ git commit -m "Initial commit"
	$ git push -u origin master

## Creating branch
	$ git branch gh-pages
	$ git push origin gh-pages

All the updated files must be merged from master to gh-pages(the name can not be changed)	

The url is built from the following pattern: <br>
[github_username].github.io/[repo_name]

## Reference
- https://www.tikalk.com/posts/2013/11/05/deploy-reveal-js-slideshow-on-github-pages/