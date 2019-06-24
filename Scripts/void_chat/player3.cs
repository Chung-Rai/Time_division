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
using System.Linq;

public class player3 : MonoBehaviour
{

    public Animator anim;
    float speed = 400f;
    string ac="None" ;
    public static bool reset=false;
    float time_f = 0f;
    int time_i = 0;
    public Text show;
    public SpriteRenderer m_Sprite;
    //public  SpriteRenderer thinking_Sprite;

    private void Start()
    {
        anim = GetComponent<Animator>();
    }
    void Update()
    {
        
        if (reset)
        {

            if (void_chat.voice.WaitUntilDone(30000) && show.text!="")
            {
                m_Sprite.sprite = (Sprite)Resources.Load<Sprite>("None");
                reset = false;
                show.text = "";
                void_chat.action = "Reset";
            }
        }
        
        if ( !(ac == void_chat.action))
        {
            switch (void_chat.action)
            {
                case "start":
                    anim.Play("WAIT02", -1, 0f);
                    ac = void_chat.action;
                    //ac = "None";
                    //void_chat.action = "None";
                    break;

                case "Move_Left":
                    //gameObject.transform.rotation = Quaternion.Euler(0f, 270f, 0f);
                    anim.Play("WALK00_B", -1, 0f);
                    ac = void_chat.action;
                    //reset = true;
                    break;

                case "Reset":
                    ac = void_chat.action;
                    if (gameObject.transform.localPosition.x > 0f)
                        anim.Play("WALK00_F", -1, 0f);
                    break;
                case "Check_itinerary":
                    //gameObject.transform.rotation = Quaternion.Euler(0f, 270f, 0f);
                    anim.Play("WALK00_B", -1, 0f);
                    //ac = void_chat.action;
                    break;

                case "Happy":
                    anim.Play("WAIT03", -1, 0f);
                    ac = void_chat.action;
                    //ac = "None";
                    //void_chat.action = "None";
                    break;

                case "Introduction":
                    anim.Play("WIN00", -1, 0f);
                    ac = void_chat.action;
                    //ac = "None";
                    //void_chat.action = "None";
                    break;
                case "greet":
                    anim.Play("JUMP01", -1, 0f);
                    ac = void_chat.action;
                    //ac = "None";
                    //void_chat.action = "None";
                    break;
                case "LIKE":
                    anim.Play("JUMP00", -1, 0f);
                    ac = void_chat.action;
                    //ac = "None";
                    //void_chat.action = "None";
                    break;

                default:
                    break;
            }
        }

        float step = speed * Time.deltaTime;

        switch (ac)
        {

            case "Reset":
                if (gameObject.transform.localPosition.x > 0f)
                {
                    gameObject.transform.localPosition = Vector3.MoveTowards(gameObject.transform.localPosition, new Vector3(-150f, 0f, 0f), step);
                }
                else if (gameObject.transform.localPosition.x <= 0f)
                {
                    ac = "None";
                    void_chat.action = "None";
                }
                break;

            default:
                break;
        }
    }
}
