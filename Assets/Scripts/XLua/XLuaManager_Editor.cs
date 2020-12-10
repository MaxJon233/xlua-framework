using System.Collections;
using System.Collections.Generic;
using UnityEngine;

#if UNITY_EDITOR
public static class XLuaManager_EditorHelper
{
    static System.Action onExit = null;

    public static void InitEditor(System.Action exit)
    {
        UnityEditor.EditorApplication.playModeStateChanged -= OnEditorPalyModeChanged;
        UnityEditor.EditorApplication.playModeStateChanged += OnEditorPalyModeChanged;
        onExit = exit;
    }

    private static void OnEditorPalyModeChanged(UnityEditor.PlayModeStateChange changed)
    {
        //点击编辑器停止的时候调用
        //if(UnityEditor.EditorApplication.isPlaying == false)
        if (changed == UnityEditor.PlayModeStateChange.ExitingPlayMode) {
            UnityEditor.EditorApplication.playModeStateChanged -= OnEditorPalyModeChanged;
            if (onExit != null) {
                onExit();
                onExit = null;
            };
        }
    }


}

#endif