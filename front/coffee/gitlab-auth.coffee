###
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos INC
###

GitLabLoginButtonDirective = ($window, $params, $location, $config, $events, $confirm,
                              $auth, $navUrls, $loader) ->
    # Login or registar a user with his/her gitlab account.
    #
    # Example:
    #     tg-gitlab-login-button()
    #
    # Requirements:
    #   - ...

    link = ($scope, $el, $attrs) ->
        auth_url = $config.get("gitLabUrl", null)
        clientId = $config.get("gitLabClientId", null)

        loginOnSuccess = (response) ->
            if $params.next and $params.next != $navUrls.resolve("login")
                nextUrl = $params.next
            else
                nextUrl = $navUrls.resolve("home")

            $events.setupConnection()

            $location.search("next", null)
            $location.search("token", null)
            $location.search("state", null)
            $location.search("code", null)
            $location.path(nextUrl)

        loginOnError = (response) ->
            $location.search("state", null)
            $location.search("code", null)
            $loader.pageLoaded()

            if response.data._error_message
                $confirm.notify("light-error", response.data._error_message )
            else
                $confirm.notify("light-error", "Our Oompa Loompas have not been able to get you
                                                credentials from GitLab.")  #TODO: i18n

        loginWithGitLabAccount = ->
            type = $params.state
            code = $params.code
            token = $params.token

            return if not (type == "gitlab" and code)
            $loader.start(true)

            url = document.createElement('a')
            url.href = $location.absUrl()
            redirectUri = "#{url.protocol}//#{url.hostname}#{if url.port == '' then '' else ':'+url.port}#{window.taigaConfig.baseHref}login"

            data = {code: code, token: token, redirectUri: redirectUri}
            $auth.login(data, type).then(loginOnSuccess, loginOnError)

        loginWithGitLabAccount()

        $el.on "click", ".button-auth", (event) ->
            url = document.createElement('a')
            url.href = $location.absUrl()
            redirectToUri = "#{url.protocol}//#{url.hostname}#{if url.port == '' then '' else ':'+url.port}#{window.taigaConfig.baseHref}login"

            url = "#{auth_url}/oauth/authorize?client_id=#{clientId}&state=gitlab&response_type=code&scope=read_user&redirect_uri=#{redirectToUri}"
            $window.location.href = url

        $scope.$on "$destroy", ->
            $el.off()

    return {
        link: link
        restrict: "EA"
        template: ""
    }

module = angular.module('taigaContrib.gitlabAuth', [])
module.directive("tgGitlabLoginButton", ["$window", '$routeParams', "$tgLocation", "$tgConfig", "$tgEvents",
                                         "$tgConfirm", "$tgAuth", "$tgNavUrls", "tgLoader",
                                         GitLabLoginButtonDirective])
