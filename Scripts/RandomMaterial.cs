using UnityEngine;
using System.Collections;

public class RandomMaterial : MonoBehaviour {

	// Use this for initialization
	void Awake () {
        GetComponent<Renderer>().material = GetRandomMaterial();
    }
	


    /// <summary>
    /// helper method to get a random color
    /// </summary>
    /// <returns></returns>
    public Material GetRandomMaterial()
    {
            return Resources.Load("Materials/grass") as Material;
    }

}
