package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"os"
	"strings"
	"time"
)

const (
	baseURL  = "http://dangkyhoc.vnu.edu.vn"
	loginURL = baseURL + "/dang-nhap"
	listURL  = baseURL + "/danh-sach-mon-hoc/1/1"
	pickURL  = baseURL + "/chon-mon-hoc/{}/1/1"
	finURL   = baseURL + "/xac-nhan-dang-ky/1"
)

func main() {
	username := os.Getenv("UET_USER")
	password := os.Getenv("UET_PASS")

	// http client prepare
	client := &http.Client{}
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
	login(client, username, password)
	maximumConcurrentGoroutines := 50
	guard := make(chan struct{}, maximumConcurrentGoroutines)

	for true {
		guard <- struct{}{}
		go func(client *http.Client) {
			register(client, []string{"573"})
			<-guard
		}(client)
		time.Sleep(50 * time.Millisecond)
	}
}

func login(client *http.Client, username string, password string) {
	payload := url.Values{}
	payload.Set("LoginName", username)
	payload.Set("Password", password)
	payload.Set("__RequestVerificationToken", "cP9Q5HM_m1WeS0umvbInUJUkQiVFO95phgxli1cln_J7C7cSnmxZcNCWGtY2_uOCE_RyVJA5tguT7AgYaG9Gc8u69CU1")
	client.PostForm(loginURL, payload)
}

func register(client *http.Client, target []string) {
	client.Post(listURL, "application/x-www-form-urlencoded", nil)
	for _, rowindex := range target {
		u := strings.ReplaceAll(pickURL, "{}", rowindex)
		client.Post(u, "application/x-www-form-urlencoded", nil)
	}
	resp, _ := client.Post(finURL, "application/x-www-form-urlencoded", nil)
	respBody, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(respBody))
}
