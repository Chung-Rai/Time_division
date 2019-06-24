using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.Net.Sockets;
using System.Text;
using System;
using UnityEngine.UI;
using UnityEngine;


public class faceRecognize: MonoBehaviour
{

    #region private members
    private TcpClient socketConnection;

    #endregion
    public InputField input;
    public Text show;
    const int RevSize = 1024;
    const int SenfSize = 1024;
    public byte[] RevBuffer = new byte[RevSize];
    public byte[] SendBuffer = new byte[SenfSize];
    string strMesg = string.Empty;


    public void TCPSocketQuit()
    {       //断开链接

        socketConnection.Close();


        Debug.Log("TCP Client has quitted!");

    }

    public void Connect2TcpServer()
    {   //链接初始化，同时使用回调函数

        try
        {
            socketConnection = new TcpClient("192.168.1.157", 8002);
            //socketConnection.GetStream().BeginRead(RevBuffer, 0, RevSize, new AsyncCallback(Listen4Data), null);

            Debug.Log("TCP Client connected!");
            SendMessage("W");
            socketConnection.GetStream().BeginRead(RevBuffer, 0, RevSize, new AsyncCallback(Listen4Data), null);
        }
        catch
        {

            Debug.Log("Open thread for build client is error!  ");

        }

    }

    public void Listen4Data(IAsyncResult ar)
    {//此为回调函数
        int BytesRead;
        /*
        try
        {
            BytesRead = socketConnection.GetStream().EndRead(ar);

            if (BytesRead < 1)
            {

                Debug.Log("Disconnected");
                return;
            }

            strMesg = Encoding.Default.GetString(RevBuffer, 0, BytesRead);
            Debug.Log(strMesg);

            socketConnection.GetStream().BeginRead(RevBuffer, 0, RevSize, new AsyncCallback(Listen4Data), null);//再次使用回掉函数

        }
        catch
        {
            Debug.Log("Disconnected");
        }
        */
        BytesRead = socketConnection.GetStream().EndRead(ar);
        strMesg = Encoding.UTF8.GetString(RevBuffer, 0, BytesRead);
        Debug.Log(strMesg);
        if(strMesg == "B")
        {
            Debug.Log("成功1");
            SendMessage("C");
            socketConnection.GetStream().BeginRead(RevBuffer, 0, RevSize, new AsyncCallback(Listen4Data), null);
        }
        if (strMesg == "D")
        {
            Debug.Log("成功2");
        }

    }

    public void SendMessage( string mode)//简单的发送数据
    {

       
        if (socketConnection == null)
        {
            Debug.Log(socketConnection);
            return;

        }
        
        try
        {
            NetworkStream stream = socketConnection.GetStream();

            if (stream.CanWrite)
            {
                string clientMessage = mode;

                //clientMessage = StringToBinary(clientMessage);
                //clientMessage = Encoding.Default.GetString(clientMessage);
                byte[] clientMessageAsByteArray = Encoding.UTF8.GetBytes(clientMessage);
                //stream.Write(SendBuffer, 0, 4);
                stream.Write(clientMessageAsByteArray, 0, clientMessage.Length);
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }
    //Char字符转成7位二进制
    public string StringToBinary(string ss)
    {
        byte[] u = Encoding.ASCII.GetBytes(ss);
        string binaryNum = string.Empty;
        string result = string.Empty;
        foreach (byte a in u)
        {

            binaryNum = Convert.ToString(a, 2);
            if (binaryNum.Length < 7)
            {
                for (int i = 0; i < 7 - binaryNum.Length; i++)
                {
                    binaryNum = '0' + binaryNum;
                }
            }
            result += binaryNum;
        }
        return result;

    }

}
