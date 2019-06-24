using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;
using System;
using System.Net.Sockets;
using System.Text;
using SpeechLib;
using System.Xml;
using System.IO;
using UnityEngine.Windows.Speech;
using System.Linq;
using System.Text.RegularExpressions;

public class void_chat : MonoBehaviour
{
    public static string action;
    public static bool motion = false;
    public Animator anim;
    public SpriteRenderer m_Sprite;
    public SpriteRenderer m_Sprite1;
    public SpriteRenderer m_Sprite2;
    public SpriteRenderer m_Sprite3;
    public InputField input;
    string _path;

    public  static DictationRecognizer dictationRecognizer;
    public Text show;
    public Text show1;
    public Text show2;
    public Text show3;
    public  Text itinerary;
    //public string say;

    public  float  time_f = 0f,clock_time_f=0f,counter_time_f=0f, remind_time_f = 0f;
    public  int time_i = 0,clock_time_i=0,counter_time_i=0, remind_time_i = 0;
    public static bool flag=false,flag_start=false;
    string adf = "0";
    string face_mode = "Face_Recognition";
    int counter_adf = 0;
    int face_flag = 0;
    int rest_count = 0;
    bool rest = true;
    bool itinerary_flag = false;
    string song_adf = "0";
    string who;
    public int mood = 0;
    public Text count_time_minute, count_time_hour, count_time_second;
    int h,m,s;
    bool train_flag = false;

    //public AudioSource _audio;
    //private SpVoice voice;
    public static SpVoice voice;
    public string[] keywords = new string[] { "小白" };
    public  ConfidenceLevel confidence = ConfidenceLevel.Medium;

    protected PhraseRecognizer recognizer;
    protected string word = "";
    public SpriteRenderer thinking_Sprite;
    //bool say_flag = false;

    private void Start()
    {
        Reminder();
        anim = GetComponent<Animator>();
        recognizer = new KeywordRecognizer(keywords, confidence);
        if (keywords != null)
        {
            recognizer.OnPhraseRecognized += Recognizer_OnPhraseRecognized;
            recognizer.Start();
            Debug.Log("開始了");
        }
    }

    private void Recognizer_OnPhraseRecognized(PhraseRecognizedEventArgs args)
    {
        word = args.text;
        //Debug.Log(word);
        voice = new SpVoice();
        voice.Volume = 100; // Volume (no xml)
        voice.Rate = 0;  //   Rate (no xml)
        voice.Speak("主人怎麼了", SpeechVoiceSpeakFlags.SVSFlagsAsync);
        //flag = true;
        
        PhraseRecognitionSystem.Shutdown();
        recognization();
        //anim.Play("WAIT02", -1, 0f); // 叫他時做的動作
        Debug.Log("小白偵測到了");
        action = "start";
        motion = true;
        rest = false;

    }

    private void OnApplicationQuit()
    {
        if (recognizer != null && recognizer.IsRunning)
        {
            recognizer.OnPhraseRecognized -= Recognizer_OnPhraseRecognized;
            recognizer.Stop();
        }
    }

    public void bu()
    {
        PhraseRecognitionSystem.Restart();
    }
    
    public  void recognization()
    {
            time_f = 0f;
            time_i = 0;
            dictationRecognizer = new DictationRecognizer();
            dictationRecognizer.DictationResult += DictationRecognizer_DictationResult;
            dictationRecognizer.DictationComplete += DictationRecognizer_DictationComplete;
            dictationRecognizer.DictationHypothesis += DictationRecognizer_DictationHypothesis;
            dictationRecognizer.DictationError += DictationRecognizer_DictationError;

            dictationRecognizer.Start();
    }
    void Update()
    {

        if (flag)
        {
            flag = false;
            recognization();
        }
        if (input.text.IndexOf("结束对话") > -1)
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的", SpeechVoiceSpeakFlags.SVSFlagsAsync);
            input.text = "";
            show.text = "";
            dictationRecognizer.Dispose();
            PhraseRecognitionSystem.Restart();
            rest = true;
           
        }
        
        if ((input.text.IndexOf("自我介绍") > -1) || (input.text.IndexOf("跟大家问好") > -1) || (input.text.IndexOf("你是谁") > -1))
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            show.text = "大家好 我的名子是小白 我是一個正在努力學習的人工智慧管家唷";
            voice.Speak(show.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
            input.text = "";
            show.text = "";
            action = "Introduction";
        }
        

        time_f += Time.deltaTime;
        time_i = (int)time_f;
        if (time_i == 2)
        {
            
            if (input.text != "")
            {
                if (face_flag == 1)
                {
                    face_recognize();
                }
                else {
                    //OnDestroy();
                    EnterPlayerName();
                }
                rest_count = 0;
            }         
            else if(!rest)
            {
                rest_count +=1;
                Debug.Log(rest_count);
                if(rest_count == 10)
                {
                    dictationRecognizer.Dispose();
                    PhraseRecognitionSystem.Restart();
                    rest_count = 0;
                    rest = true;
                    Debug.Log("休息");
                }
            }
            
            time_f = 0f;
            time_i = 0;
        }
        
        clock_time_f += Time.deltaTime;
        clock_time_i = (int)clock_time_f;
        if (clock_time_i == 5)
        {       
            clock_time_f = 0f;
            clock_time_i = 0;
            //clock();
            Reminder();
            //charactormood(); //呼叫肚子餓
        }
        
    }

    string loadXMLStandalone(string fileName)
    {

        string path = Path.Combine("Resources", fileName);
        path = Path.Combine(Application.dataPath, path);
        Debug.Log("Path:  " + path);
        StreamReader streamReader = new StreamReader(path);
        string streamString = streamReader.ReadToEnd();
        Debug.Log("STREAM XML STRING: " + streamString);
        return streamString;
    }

    void OnGUI()
    {

        SpObjectTokenCategory tokenCat = new SpObjectTokenCategory();
        tokenCat.SetId(SpeechLib.SpeechStringConstants.SpeechCategoryVoices, false);
        ISpeechObjectTokens tokens = tokenCat.EnumerateTokens(null, null);
    }

    public void EnterPlayerName()
    {
        if (input.text.IndexOf("天气") > -1 || input.text.IndexOf("空气") > -1 || input.text.IndexOf("晾衣服") > -1)
        {
            action = "Move_Left";
        }
        else if (input.text.IndexOf("有什么事吗") > -1 )
        {
            itinerary_flag = true;
        }
        else
        {
            thinking_Sprite.sprite = (Sprite)Resources.Load<Sprite>("wait");
        }
          
        if (input.text.IndexOf("叫我") > -1)
        {
            _path = "http://140.128.88.198:5000/counter/";//初始化URL
            _path += WWW.EscapeURL(input.text);//中文轉url編碼
            StartCoroutine("count");
            input.text = "";
        }
        else
        {

            _path = "http://140.128.88.198:5000/chat_ar/";//初始化URL
            _path += adf + "/";
            _path += WWW.EscapeURL(input.text);//中文轉url編碼
            input.text = "";
            StartCoroutine("chat");

        }
    }
    IEnumerator chat()
    {
        WWW www = new WWW(_path);
        yield return www;
        adf = www.text;
        
        if (adf == "1")
        {
 
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的你要新增甚麼時候", SpeechVoiceSpeakFlags.SVSFlagsAsync);

        }       
        else if (adf == "14")
        {
            //show.text = "請告訴我時間點";
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("請告訴我時間點", SpeechVoiceSpeakFlags.SVSFlagsAsync);


        }
        else if (adf =="2")
        {
            //show.text = "好的你要新增甚麼事件";
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的你要新增甚麼事件", SpeechVoiceSpeakFlags.SVSFlagsAsync);


        }
        else if (adf =="3")
        {
            //show.text = "好的你要甚麼時候叫你呢";
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的你要甚麼時候叫你呢", SpeechVoiceSpeakFlags.SVSFlagsAsync);


        }
        else if (adf == "4")
        {
            //show.text = "最近有安排其他行程確定還要新增行程嗎";
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("最近有安排其他行程確定還要新增行程嗎", SpeechVoiceSpeakFlags.SVSFlagsAsync);


        }
        else if(adf == "11")
        {
            //show.text = "好的你要刪除甚麼時候或甚麼事件呢";
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的你要刪除甚麼時候或甚麼事件呢", SpeechVoiceSpeakFlags.SVSFlagsAsync);


        }
        else if (adf == "13")
        {
            check_deitinerary();

        }
        else if (adf == "9")
        {
            check_itinerary();
        }
        else if (adf == "5")
        {
            song_adf = "1";
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的要聽什麼", SpeechVoiceSpeakFlags.SVSFlagsAsync);


        }
        else if (adf == "6")
        {
            youtube_mov();
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的", SpeechVoiceSpeakFlags.SVSFlagsAsync);


        }
        else if(adf == "7")
        {
            face_flag = 1;
            face_recognize();
            adf = "0";
        }
        else if(adf == "8")
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的", SpeechVoiceSpeakFlags.SVSFlagsAsync);
            Application.LoadLevel("rotatedPathsLevel");


        }
        else if (adf == "10")
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的你要查詢哪時候或甚麼事件呢", SpeechVoiceSpeakFlags.SVSFlagsAsync);
            itinerary_flag = true;
        }
        else if (adf == "15")
        {
            wiki();
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的", SpeechVoiceSpeakFlags.SVSFlagsAsync);



        }
        else if (adf == "16" || adf =="18")
        {

            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("是否要為你開燈?", SpeechVoiceSpeakFlags.SVSFlagsAsync);


        }
        else if (adf == "17")
        {

            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("好的，你想開哪裡的電燈?", SpeechVoiceSpeakFlags.SVSFlagsAsync);
        }
        else if (adf == "19")
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("我不懂，請問是甚麼意思", SpeechVoiceSpeakFlags.SVSFlagsAsync);

        }
        else if (adf == "20")
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("請問目的站和終點站是哪裡", SpeechVoiceSpeakFlags.SVSFlagsAsync);

        }
        else if (adf == "21")
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("請問要查詢哪時候", SpeechVoiceSpeakFlags.SVSFlagsAsync);
            train_flag = true;

        }
        else
        {
            if (song_adf=="1")
            {
                Application.OpenURL("https://www.youtube.com/"+www.text);
                song_adf = "0";
                adf = "0";
                voice = new SpVoice();
                voice.Volume = 100; // Volume (no xml)
                voice.Rate = 0;  //   Rate (no xml)
                voice.Speak("好的", SpeechVoiceSpeakFlags.SVSFlagsAsync);
            }
            else
            {
                adf = "0";
                if (www.text.IndexOf("天氣") > -1)
                {
                    if (www.text.IndexOf("晴時多雲") > -1)
                    {
                        m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("sun");
                        m_Sprite2.sprite = (Sprite)Resources.Load<Sprite>("sun");
                    }
                    else if (www.text.IndexOf("陰時多雲短暫陣雨或雷雨") > -1 || www.text.IndexOf("陰短暫陣雨或雷雨") > -1)
                    {
                        m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("rain_light");
                        m_Sprite2.sprite = (Sprite)Resources.Load<Sprite>("rain_light");
                    }
                    else if (www.text.IndexOf("多雲時陰") > -1 || www.text.IndexOf("陰時多雲") > -1)
                    {
                        m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("gray_cloud");
                        m_Sprite2.sprite = (Sprite)Resources.Load<Sprite>("gray_cloud");
                    }
                    else if (www.text.IndexOf("多雲短暫雨") > -1 || www.text.IndexOf("多雲時陰短暫雨") > -1 || www.text.IndexOf("多雲短暫陣雨") > -1)
                    {
                        m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("cloud_rain");
                        m_Sprite2.sprite = (Sprite)Resources.Load<Sprite>("cloud_rain");
                    }
                    else if (www.text.IndexOf("多雲時晴") > -1)
                    {
                        m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("sun_cloud");
                        m_Sprite2.sprite = (Sprite)Resources.Load<Sprite>("sun_cloud");
                    }
                    else if (www.text.IndexOf("陰短暫雨") > -1 || www.text.IndexOf("陰時多雲短暫雨") > -1 || www.text.IndexOf("陰有雨") > -1 || www.text.IndexOf("陰短暫陣雨") > -1)
                    {
                        m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("cloud_rain");
                        m_Sprite2.sprite = (Sprite)Resources.Load<Sprite>("cloud_rain");
                    }
                    else if (www.text.IndexOf("多雲") > -1)
                    {
                        m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("cloud");
                        m_Sprite2.sprite = (Sprite)Resources.Load<Sprite>("cloud");
                    }
                    else if (www.text.IndexOf("陰天") > -1)
                    {
                        m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("gray_cloud");
                        m_Sprite2.sprite = (Sprite)Resources.Load<Sprite>("gray_cloud");
                    }

                    show.text = www.text;
                    show.fontSize = 15;

                    show2.text = www.text;
                    show2.fontSize = 15;

                    voice = new SpVoice();
                    voice.Volume = 100; // Volume (no xml)
                    voice.Rate = 0;  //   Rate (no xml)
                    voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);

                    //recognization();

                }
                else if(itinerary_flag == true)
                {
                    action = "Move_Left";

                    show.text = www.text;
                    show.fontSize = 15;

                    show2.text = www.text;
                    show2.fontSize = 15;

                    voice = new SpVoice();
                    voice.Volume = 100; // Volume (no xml)
                    voice.Rate = 0;  //   Rate (no xml)
                    voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
                    itinerary_flag = false;
                    //recognization();


                }
                else if(www.text.IndexOf("高兴") > -1)
                {
                    action = "Happy";
                    voice = new SpVoice();
                    voice.Volume = 100; // Volume (no xml)
                    voice.Rate = 0;  //   Rate (no xml)
                    voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
                }
                else if (www.text.IndexOf("早安") > -1 || www.text.IndexOf("你好") > -1)
                {
                    action = "greet";
                    voice = new SpVoice();
                    voice.Volume = 100; // Volume (no xml)
                    voice.Rate = 0;  //   Rate (no xml)
                    voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
                }
                else if (www.text.IndexOf("喜欢") > -1)
                {
                    action = "LIKE";
                    voice = new SpVoice();
                    voice.Volume = 100; // Volume (no xml)
                    voice.Rate = 0;  //   Rate (no xml)
                    voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
                }
                else if (www.text.IndexOf("空气") > -1)
                {
                    show.text = www.text;
                    show.fontSize = 15;

                    show2.text = www.text;
                    show2.fontSize = 15;

                    voice = new SpVoice();
                    voice.Volume = 100; // Volume (no xml)
                    voice.Rate = 0;  //   Rate (no xml)
                    voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);

                }
                else if (train_flag)
                {
                    action = "Move_Left";
                    show.text = www.text;
                    show.fontSize = 15;

                    show2.text = www.text;
                    show2.fontSize = 15;

                    voice = new SpVoice();
                    voice.Volume = 100; // Volume (no xml)
                    voice.Rate = 0;  //   Rate (no xml)
                    voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
                }
                else
                {
                   
                    //show.text = www.text;
                    adf = "0";
                    voice = new SpVoice();
                    voice.Volume = 100; // Volume (no xml)
                    voice.Rate = 0;  //   Rate (no xml)
                    voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);

                    //voice.WaitUntilDone(10000); 
                    //dictationRecognizer.Start();
                    //recognization();
                    
                    
                }

            }
   

        }
        
        thinking_Sprite.sprite = (Sprite)Resources.Load<Sprite>("None");
        input.text = "";
        //recognization();
    }

    IEnumerator count()
    {
        show.text = "";
        WWW www = new WWW(_path);
        yield return www;
        Int32.TryParse(www.text, out s);
        /*
        m = s / 60;
        if(m >=60)
        {
            h = m / 60;
            m = m % 60;
            s = s % 60;
        }
        else
        {
            h = 0;
            s = s % 60;
        }
        counter_adf = 1;
        show.text ="好的";
        voice = new SpVoice();
        voice.Volume = 100; // Volume (no xml)
        voice.Rate = 0;  //   Rate (no xml)
        voice.Speak(show.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
        */
        voice = new SpVoice();
        voice.Volume = 100; // Volume (no xml)
        voice.Rate = 0;  //   Rate (no xml)
        voice.Speak("好的", SpeechVoiceSpeakFlags.SVSFlagsAsync);
        //recognization();
        thinking_Sprite.sprite = (Sprite)Resources.Load<Sprite>("None");
        InvokeRepeating("timer", 1, 1);
    }
    void timer()
    {
        /*
        if (s == 0)
        {
            if (m == 0)
            {
                h -= 1;
                m = 59;
                s = 59;
            }
            else
            {
                m -= 1;
                s = 59;
            }

        }

        s -= 1;
        count_time_hour.text = h + "";
        count_time_minute.text = m + "";
        count_time_second.text = s + "";
        if (s == 0 && m==0 && h==0)
        {

            show.text = "主人時間到了唷";
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak(show.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);

            CancelInvoke("timer");

        }
        */
        Debug.Log(s);
        s -= 1;
        if (s == 0)
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("主人時間到了唷", SpeechVoiceSpeakFlags.SVSFlagsAsync);
            CancelInvoke("timer");
        }

    }


    private void DictationRecognizer_DictationResult(string text, ConfidenceLevel confidence)
    {
        input.text = text;
        

    }
    private void DictationRecognizer_DictationHypothesis(string text)
    {
            
            time_f = 0f;
            time_i = 0;
 

    }
    private void DictationRecognizer_DictationComplete(DictationCompletionCause cause)
    {
            
    }
    private void DictationRecognizer_DictationError(string error, int hresult)
    {

    }

    void OnDestroy()
    {

            dictationRecognizer.DictationResult -= DictationRecognizer_DictationResult;
            dictationRecognizer.DictationComplete -= DictationRecognizer_DictationComplete;
            dictationRecognizer.DictationHypothesis -= DictationRecognizer_DictationHypothesis;
            dictationRecognizer.DictationError -= DictationRecognizer_DictationError;
            dictationRecognizer.Dispose();
    }

    private AudioSource clock_alarm_music;
    private int clock_flag = 1;

    public void clock()
    {
        _path = "http://140.128.88.198:5000/clock";
        StartCoroutine("alarm_clock");
    }
    IEnumerator alarm_clock()
    {
        WWW www = new WWW(_path);
        yield return www;
        //Debug.Log(www.text);
        if((www.text=="1") & (clock_flag == 1))
        {
            clock_alarm_music = GameObject.FindGameObjectWithTag("alarm_music").GetComponent<AudioSource>();
            clock_alarm_music.Stop();
            clock_alarm_music.Play();
            clock_flag = 0;
        }
        if(www.text == "0")
        {
            clock_flag = 1;
        }


    }

    private int Remind_flag = 1;
    public void Reminder()
    {
        _path = "http://140.128.88.198:5000/Reminder";
        StartCoroutine("Remind");
    }
    IEnumerator Remind()
    {
        WWW www = new WWW(_path);
        yield return www;
        //Debug.Log(www.text);
        if (www.text == "0")
        {
            itinerary.text = "查無行程";
        }
        else
        {
            itinerary.text = www.text;
        }
    }

    public void youtube_mov()
    {
        _path = "http://140.128.88.198:5000/youtube_play";
        StartCoroutine("music");
    }
    IEnumerator music()
    {
        WWW www = new WWW(_path);
        yield return www;
        Application.OpenURL("https://www.youtube.com/" + www.text);
    }

    public void stop_clock()
    {
        clock_alarm_music = GameObject.FindGameObjectWithTag("alarm_music").GetComponent<AudioSource>();
        clock_alarm_music.Stop();
    }

    public void youtube()
    {
         Application.OpenURL("https://zh.wikipedia.org/wiki/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD");
       
    }
    public void face_recognize()
    {
        dictationRecognizer.Stop();
        _path = "http://192.168.1.157:5000/Face_Recognize/";
        if (face_mode== "Face_Recognition")
        {
            _path = "http://192.168.1.157:5000/Face_Recognize/Face_Recognition/None";
        }
        else
        {
            _path += face_mode + "/" + input.text;
        }
        StartCoroutine("name");
        input.text = "";//防延遲
    }
    IEnumerator name()
    {
        WWW www = new WWW(_path);
        yield return www;
        
        if(www.text =="False_Recognize")
        {
            show.text = "是否要認識對方";
            face_mode = "Confire_Create";
        }
        else if (www.text == "No_Face")
        {
            show.text = "沒有看到人臉";
            face_flag = 0;
        }
        else if (www.text == "Not_Learn")
        {
            show.text = "好的";
            face_flag = 0;
            face_mode = "Face_Recognition";
        }
        else if (www.text =="True_Learn")
        {
            show.text = "請告訴我您的名字";
            face_mode = "Learn_Face";
        }
        /*
        else if (www.text == "Create_Success")
        {
            show.text = "已經訓練好了唷";
            face_flag = 0;
            face_mode = "Face_Recognition";
            //face_recognize();
        }
        */
        else
        {
            show.text = www.text ;
            face_flag = 0;
            face_mode = "Face_Recognition";
        }

        voice = new SpVoice();
        voice.Volume = 100; // Volume (no xml)
        voice.Rate = 0;  //   Rate (no xml)
        voice.Speak(show.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
        input.text = "";
        //dictationRecognizer.Start();
    }
    public void check_itinerary()
    {
        _path = "http://140.128.88.198:5000/check_itinerary";
        StartCoroutine("check_itiner");
    }
    IEnumerator check_itiner()
    {
        action = "Move_Left";
        WWW www = new WWW(_path);
        yield return www;
        RectTransform rectTransform;

        voice = new SpVoice();
        voice.Volume = 100; // Volume (no xml)
        voice.Rate = 0;  //   Rate (no xml)
        voice.Speak(www.text, SpeechVoiceSpeakFlags.SVSFlagsAsync);
        show.text = www.text;

        show.fontSize = 30;
        rectTransform = show.GetComponent<RectTransform>();
        rectTransform.localPosition = new Vector3(-435, 29, 0);
        rectTransform.sizeDelta = new Vector2(361, 0);
        
        //recognization();

    }
    public void check_deitinerary()
    {
        _path = "http://140.128.88.198:5000/itinerary";
        StartCoroutine("check_deitiner");
    }
    IEnumerator check_deitiner()
    {
        WWW www = new WWW(_path);
        yield return www;
        show.text = www.text;
        if (www.text== "0"){
            adf = "0";
            show.text = "查無行程";
        }
        else
        {
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("確定是"+www.text+"嗎", SpeechVoiceSpeakFlags.SVSFlagsAsync);
        }
        //voice.WaitUntilDone(10000);
        //recognization();

    }
    private void charactormood()
    {
        DateTime now = DateTime.Now;
        if (((now.Hour == 7) |( now.Hour==12 )| (now.Hour == 18)) && (mood==0))
        {
            
            voice = new SpVoice();
            voice.Volume = 100; // Volume (no xml)
            voice.Rate = 0;  //   Rate (no xml)
            voice.Speak("肚子餓了", SpeechVoiceSpeakFlags.SVSFlagsAsync);
            
            //Debug.Log("現在時間:"+now.Hour.ToString());
        }
    }

    public void wiki()
    {
        _path = "http://140.128.88.198:5000/wiki";
        StartCoroutine("search");
    }
    IEnumerator search()
    {
        WWW www = new WWW(_path);
        yield return www;
        Application.OpenURL("https://www.google.com/search?q=" + WWW.EscapeURL(www.text));
    }
}

