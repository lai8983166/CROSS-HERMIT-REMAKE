
void FUN__text__0052b019(undefined4 param_1)

{
  code *pcVar1;
  code *pcVar2;
  code *pcVar3;
  int iVar4;
  
  pcVar2 = DAT_005922c8;
  if (API_D3D8_DLL_DebugSetMute == (code *)0x0) {
    if (DAT_008097a4 != (code *)0x0) goto LAB__text__0052b0a2;
    iVar4 = (*DAT_005922c8)("d3d8.dll");
    pcVar3 = DAT_005922cc;
    pcVar1 = DAT_00592184;
    if (iVar4 != 0) {
      iVar4 = (*DAT_00592184)("d3d8.dll");
      if (iVar4 != 0) {
        API_D3D8_DLL_DebugSetMute = (code *)(*pcVar3)(iVar4,"DebugSetMute");
      }
    }
    iVar4 = (*pcVar2)("d3d8d.dll");
    if (iVar4 != 0) {
      iVar4 = (*pcVar1)("d3d8d.dll");
      if (iVar4 != 0) {
        DAT_008097a4 = (code *)(*pcVar3)(iVar4,"DebugSetMute");
      }
    }
    if (API_D3D8_DLL_DebugSetMute != (code *)0x0) goto LAB__text__0052b08e;
  }
  else {
LAB__text__0052b08e:
    (*API_D3D8_DLL_DebugSetMute)(param_1);
  }
  if (DAT_008097a4 == (code *)0x0) {
    return;
  }
LAB__text__0052b0a2:
                    /* WARNING: Could not recover jumptable at 0x0052b0a2. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_008097a4)();
  return;
}

