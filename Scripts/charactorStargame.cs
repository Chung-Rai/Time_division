using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Assets.Scripts;
using System.Threading;

public class charactorStargame : MonoBehaviour {

    // Use this for initialization
    //character model found in https://www.assetstore.unity3d.com/en/#!/content/3012

    private Vector3 moveDirection = Vector3.zero;
    public float gravity = 20f;
    private CharacterController controller;
    public static Animator anim;

    public float JumpSpeed = 8.0f;
    public float Speed = 6.0f;
    public Transform CharacterGO;

    int rotate = 0;
    float rotationRight = 90;
    float rotationLeft = -90;
    float rotationspeed = 320;

    bool isInSwipeArea;


    IInputDetector inputDetector = null;

    // Use this for initialization
    void Start()
    {
        moveDirection = transform.forward;
        moveDirection = transform.TransformDirection(moveDirection);
        moveDirection *= Speed;

        UIManager.Instance.ResetScore();
        UIManager.Instance.SetStatus(Constants.StatusTapToStart);

        GameManager.Instance.GameState = GameState.Start;

        anim = CharacterGO.GetComponent<Animator>();
        inputDetector = GetComponent<IInputDetector>();
        controller = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {

        switch (GameManager.Instance.GameState)
        {
            case GameState.Start:
                if (Input.GetMouseButtonUp(0))
                {
                    
                    //anim.SetBool(Constants.AnimationStarted, true);
                    var instance = GameManager.Instance;
                    instance.GameState = GameState.Playing;

                    UIManager.Instance.SetStatus(string.Empty);
                    anim.Play("RUN00_F", -1, 0f);
                    anim.SetBool(Constants.AnimationStarted, false);
                }
                break;
            case GameState.Playing:
                // UIManager.Instance.IncreaseScore(0.001f);

                CheckHeight();

                DetectJumpOrSwipeLeftRight();
               
                //apply gravity
                moveDirection.y -= gravity * Time.deltaTime;
                //move the player
                controller.Move(moveDirection * Time.deltaTime);
                    break;

            case GameState.Dead:
                anim.SetBool(Constants.AnimationStarted, true);
                if (Input.GetMouseButtonUp(0))
                {
                    //restart
                    SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
                }
                break;
            default:
                break;
        }

    }

    private void CheckHeight()
    {
        if (transform.position.y < -10)
        {
            GameManager.Instance.Die();
        }
    }

    private void DetectJumpOrSwipeLeftRight()
    {
        var inputDirection = inputDetector.DetectInputDirection();
        if (controller.isGrounded && inputDirection.HasValue && inputDirection == InputDirection.Top)
        {
            moveDirection.y = JumpSpeed;
            //anim.SetBool(Constants.AnimationJump, true);
            anim.Play("JUMP00", -1, 0f);
        }
        /*else
        {
            anim.SetBool(Constants.AnimationJump, false);
        }*/


        if ((GameManager.Instance.CanSwipe && inputDirection.HasValue &&
         controller.isGrounded && inputDirection == InputDirection.Right) || rotate ==1)
        {
            float rotation = rotationspeed * Time.deltaTime;
                if(rotationRight >=0)
                {
                    rotationRight -= rotation;
                    rotate = 1;
                    if(rotationRight <= 0)
                    {
                        transform.Rotate(0, rotationRight+rotation, 0);
                        moveDirection = Quaternion.AngleAxis(rotationRight + rotation, Vector3.up) * moveDirection;
                        //allow the user to swipe once per swipe location
                        GameManager.Instance.CanSwipe = false;
                    }
                    else
                    {
                        transform.Rotate(0, rotation, 0);
                        moveDirection = Quaternion.AngleAxis(rotation, Vector3.up) * moveDirection;
                        //allow the user to swipe once per swipe location
                        GameManager.Instance.CanSwipe = false;
                    }

                }
                else
                {
                    rotate = 0;
                    rotationRight = 90;
                }
                
        }
        else if ((GameManager.Instance.CanSwipe && inputDirection.HasValue &&
         controller.isGrounded && inputDirection == InputDirection.Left) || rotate==2)
        {
            float rotation = rotationspeed * Time.deltaTime;
                if (rotationLeft <= 0)
                {
                    rotationLeft += rotation;
                    rotate = 2;
                    if (rotationLeft >= 0)
                    {
                        transform.Rotate(0, rotationLeft - rotation, 0);
                        moveDirection = Quaternion.AngleAxis(rotationLeft - rotation, Vector3.up) * moveDirection;
                        //allow the user to swipe once per swipe location
                        GameManager.Instance.CanSwipe = false;
                    }
                    else
                    {
                        transform.Rotate(0, -rotation, 0);
                        moveDirection = Quaternion.AngleAxis(-rotation, Vector3.up) * moveDirection;
                        //allow the user to swipe once per swipe location
                        GameManager.Instance.CanSwipe = false;
                    }

                }
                else
                {
                    rotate = 0;
                    rotationLeft = -90;
                }
        }


    }
}
