/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (c) 2021-present Kaleidos Ventures SL
 */

angular.module("templates").run(["$templateCache",function($templateCache){$templateCache.put("/plugins/gitlab-auth/gitlab-auth.html",'\n<div tg-gitlab-login-button="tg-gitlab-login-button"><a href="" title="Enter with your gitlab account" class="button button-auth"><img src="/plugins/gitlab-auth/images/gitlab-logo.png"/><span>Sign in with GitLab</span></a></div>')}]),function(){var GitLabLoginButtonDirective,module;GitLabLoginButtonDirective=function($window,$params,$location,$config,$events,$confirm,$auth,$navUrls,$loader){var link;return link=function($scope,$el,$attrs){var auth_url,clientId,loginOnError,loginOnSuccess,loginWithGitLabAccount;return auth_url=$config.get("gitLabUrl",null),clientId=$config.get("gitLabClientId",null),loginOnSuccess=function(response){var nextUrl;return nextUrl=$params.next&&$params.next!==$navUrls.resolve("login")?$params.next:$navUrls.resolve("home"),$events.setupConnection(),$location.search("next",null),$location.search("token",null),$location.search("state",null),$location.search("code",null),$location.path(nextUrl)},loginOnError=function(response){return $location.search("state",null),$location.search("code",null),$loader.pageLoaded(),response.data._error_message?$confirm.notify("light-error",response.data._error_message):$confirm.notify("light-error","Our Oompa Loompas have not been able to get you credentials from GitLab.")},loginWithGitLabAccount=function(){var code,data,redirectUri,token,type,url;if(type=$params.state,code=$params.code,token=$params.token,"gitlab"===type&&code)return $loader.start(!0),url=document.createElement("a"),url.href=$location.absUrl(),redirectUri=url.protocol+"//"+url.hostname+(""===url.port?"":":"+url.port)+"/login",data={code:code,token:token,redirectUri:redirectUri},$auth.login(data,type).then(loginOnSuccess,loginOnError)},loginWithGitLabAccount(),$el.on("click",".button-auth",function(event){var redirectToUri,url;return url=document.createElement("a"),url.href=$location.absUrl(),redirectToUri=url.protocol+"//"+url.hostname+(""===url.port?"":":"+url.port)+"/login",url=auth_url+"/oauth/authorize?client_id="+clientId+"&state=gitlab&response_type=code&scope=read_user&redirect_uri="+redirectToUri,$window.location.href=url}),$scope.$on("$destroy",function(){return $el.off()})},{link:link,restrict:"EA",template:""}},module=angular.module("taigaContrib.gitlabAuth",[]),module.directive("tgGitlabLoginButton",["$window","$routeParams","$tgLocation","$tgConfig","$tgEvents","$tgConfirm","$tgAuth","$tgNavUrls","tgLoader",GitLabLoginButtonDirective])}.call(this);