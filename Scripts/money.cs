using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class money : MonoBehaviour {
    public string _path;
    public Text coin;
	// Use this for initialization
	void Start () {

        getcoin();
    }
	
	// Update is called once per frame
	void Update () {

	}
    public void getcoin()
    {

        _path = "http://140.128.88.198:5000/getmoney/";//初始化URL
        _path += sign_in.id;
        StartCoroutine("getc");
    }
    IEnumerator getc()
    {
        WWW www = new WWW(_path);
        yield return www;
        Debug.Log(www.text);
        coin.text = www.text;
    }
}
