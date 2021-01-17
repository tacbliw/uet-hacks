package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"os"
	"strings"
	"time"
)

const (
	baseURL       = "http://dangkyhoc.vnu.edu.vn"
	loginURL      = baseURL + "/dang-nhap"
	listURL       = baseURL + "/danh-sach-mon-hoc/1/1"
	registeredURL = baseURL + "/danh-sach-mon-hoc-da-dang-ky/1"
	pickURL       = baseURL + "/chon-mon-hoc/{}/1/1"
	finURL        = baseURL + "/xac-nhan-dang-ky/1"
)

var (
	loggedIn = false
)

func main() {
	username := os.Args[1]
	password := os.Args[2]

	// http client prepare
	client := &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
	defer client.CloseIdleConnections()

	cookieJar, _ := cookiejar.New(nil)
	tokenCookie := &http.Cookie{
		Name:     "__RequestVerificationToken",
		Value:    "Bx1tfbILleOSxmTmKVL7WRAn-hxweyUf44kSUtjXShMkipaWGrHnpl5ipb6RxHDGdBh-tgQnii0bqbFzscdO80AuB4s1",
		HttpOnly: false,
	}
	u, _ := url.Parse(baseURL)
	cookieJar.SetCookies(u, []*http.Cookie{tokenCookie})
	client.Jar = cookieJar

	// doit
	loginSuccess := false
	for !loginSuccess {
		loginSuccess = login(client, username, password)
		time.Sleep(10 * time.Second)
	}
	loggedIn = true
	fmt.Println("Login Success")
	fmt.Println(client.Jar)

	go sessionGuard(client, username, password)

	maximumConcurrentGoroutines := 100
	guard := make(chan struct{}, maximumConcurrentGoroutines)

	for true {
		guard <- struct{}{}
		go func(client *http.Client) {
			_ = register(client, os.Args[3:])
			<-guard
		}(client)
		time.Sleep(1 * time.Second)
	}
}

func login(client *http.Client, username string, password string) bool {
	payload := url.Values{}
	payload.Set("LoginName", username)
	payload.Set("Password", password)
	payload.Set("__RequestVerificationToken", "cP9Q5HM_m1WeS0umvbInUJUkQiVFO95phgxli1cln_J7C7cSnmxZcNCWGtY2_uOCE_RyVJA5tguT7AgYaG9Gc8u69CU1")
	resp, err := client.PostForm(loginURL, payload)
	if err != nil {
		fmt.Println(err)
		return false
	}
	defer resp.Body.Close()
	if resp.StatusCode != 302 {
		fmt.Println("Login failed")
		return false
	}
	resp2, err := client.Post(listURL, "application/x-www-form-urlencoded", nil)
	if err != nil {
		fmt.Println(err)
		return false
	}
	defer resp2.Body.Close()
	if resp2.StatusCode != 200 {
		fmt.Println("Got service unavailable")
		return false
	}
	return true
}

func register(client *http.Client, targets []string) bool {
	var err error
	var resp *http.Response
	if !loggedIn {
		time.Sleep(10 * time.Second)
		return false
	}
	for _, target := range targets {
		u := strings.ReplaceAll(pickURL, "{}", target)
		resp, err = client.Post(u, "application/x-www-form-urlencoded", nil)
		if err != nil {
			fmt.Println(err)
			return false
		}
		io.Copy(ioutil.Discard, resp.Body)
		resp.Body.Close()
	}
	resp2, err := client.Post(finURL, "application/x-www-form-urlencoded", nil)
	if err != nil {
		fmt.Println(err)
		return false
	}
	if resp2.StatusCode == 302 {
		fmt.Println("Got redirect, session expired")
		loggedIn = false
		return false
	}
	respBody, _ := ioutil.ReadAll(resp2.Body)
	fmt.Println(string(respBody))
	resp2.Body.Close()
	return true
}

func sessionGuard(client *http.Client, username string, password string) {
	for true {
		if !loggedIn {
			fmt.Print("Attempting to re-login... ")
			loggedIn = login(client, username, password)
		}
		time.Sleep(10 * time.Second)
	}
}
