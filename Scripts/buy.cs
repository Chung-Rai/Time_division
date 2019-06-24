using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class buy : MonoBehaviour {


    public string _path;
    public Text much;
    public void costmony()
    {

        _path = "http://140.128.88.198:5000/costmoney/";//初始化URL
        _path += sign_in.id + "/" + much.text;
        StartCoroutine("cost");
    }
    IEnumerator cost()
    {
        WWW www = new WWW(_path);
        yield return www;
        Debug.Log(www.text);
    }
    public void goshop()
    {
        Application.LoadLevel("shop");
    }
    public void gohome()
    {
        Application.LoadLevel("main");
    }
}
