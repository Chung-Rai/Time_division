using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class UIManager : MonoBehaviour
{

    void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else
        {
            DestroyImmediate(this);
        }
    }

    //singleton implementation
    private static UIManager instance;
    public static UIManager Instance
    {
        get
        {
            if (instance == null)
                instance = new UIManager();
            
            return instance;
        }
    }

    protected UIManager()
    {
    }

    public float score = 0;


    public void ResetScore()
    {
        score = 0;
        UpdateScoreText();
    }
    
    public void SetScore(float value)
    {
        score = value;
        UpdateScoreText();
    }

    public void IncreaseScore(float value)
    {
        score += value;
        UpdateScoreText();
        insetcoin();

    }
    
    private void UpdateScoreText()
    {
        ScoreText.text = score.ToString();

    }

    public void SetStatus(string text)
    {
        StatusText.text = text;
    }

    public Text ScoreText, StatusText;

    public string _path;
    public void insetcoin()
    {

        _path = "http://140.128.88.198:5000/insertmoney/";//初始化URL
        _path += sign_in.id + "/" + score.ToString();
        StartCoroutine("insert");
    }
    IEnumerator insert()
    {
        WWW www = new WWW(_path);
        yield return www;
        Debug.Log(www.text);
    }

}
