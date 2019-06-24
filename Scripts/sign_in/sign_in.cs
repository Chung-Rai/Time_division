using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class sign_in : MonoBehaviour {

    public string _path;
    public InputField account;
    public  InputField password;
    public static string id;
    public static string pw;

    public Text show;

    public void EnterPlayerName()
    {
        _path = "http://140.128.88.198:5000/login/";//初始化URL
        _path += account.text + "/" + password.text;
        id = account.text;
        pw = password.text;
        Debug.Log(_path);
        StartCoroutine("login");
    }
    IEnumerator login()
    {
        WWW www = new WWW(_path);
        yield return www;
        Debug.Log(www.text); 
        show.text = www.text;
        if (show.text == id)
        {
            //Application.LoadLevel("main");
            Application.LoadLevel("main");
        }
    }
}
