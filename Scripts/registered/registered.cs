using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Text.RegularExpressions;

public class registered : MonoBehaviour
{
    public string _path;
    public InputField account;
    public InputField password;
    public InputField email;
    public Text show;

    public void EnterPlayerName()
    {
        
        _path = "http://140.128.88.198:5000/registered/";//初始化URL
        _path += account.text + "/" + password.text+"/" + email.text;
        if (IsValidEMailAddress(email.text))
        {
            Debug.Log(_path);
            StartCoroutine("registereds");
        }
        else
            show.text = "e-mail格式錯誤";
    }

    public static bool IsValidEMailAddress(string email)
    {
        return Regex.IsMatch(email, @"^([\w-]+\.)*?[\w-]+@[\w-]+\.([\w-]+\.)*?[\w]+$");
    }

    IEnumerator registereds()
    {
        WWW www = new WWW(_path);
        yield return www;
        Debug.Log(www.text);
        show.text = www.text;
    }
}
