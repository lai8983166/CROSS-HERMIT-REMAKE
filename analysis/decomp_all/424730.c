
void __thiscall FUN__text__00424730(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (param_2 != 0) {
    *(int *)(param_1 + 4) = param_2;
    local_8 = param_1;
    (*API_USER32_DLL_GetWindowLongA)(*(undefined4 *)(param_1 + 4),4);
    iVar3 = FUN__text__0056ce80();
    if (iVar3 == 0) {
      *(undefined4 *)(local_8 + 0xc) = 0;
    }
    else {
      *(undefined4 *)(local_8 + 0xc) = 1;
    }
    (*API_USER32_DLL_SetPropA)(*(undefined4 *)(local_8 + 4),"CPP_CLASS",local_8);
    FUN__text__0056ce80();
    local_c = (-(uint)(*(int *)(local_8 + 0xc) != 0) & 8) - 4;
    local_10 = param_3;
    if (param_3 == 0) {
      (*API_USER32_DLL_GetWindowLongA)(*(undefined4 *)(local_8 + 4),local_c);
      pcVar1 = (code *)FUN__text__0056ce80();
      if (pcVar1 != FUN__text__00424980) {
        (*API_USER32_DLL_SetWindowLongA)(*(undefined4 *)(local_8 + 4),local_c,FUN__text__00424980);
        uVar2 = FUN__text__0056ce80();
        *(undefined4 *)(local_8 + 8) = uVar2;
      }
    }
    else if (param_3 == 1) {
      (*API_USER32_DLL_GetWindowLongA)(*(undefined4 *)(local_8 + 4),local_c);
      pcVar1 = (code *)FUN__text__0056ce80();
      if (pcVar1 != FUN__text__00424b20) {
        (*API_USER32_DLL_SetWindowLongA)(*(undefined4 *)(local_8 + 4),local_c,FUN__text__00424b20);
        uVar2 = FUN__text__0056ce80();
        *(undefined4 *)(local_8 + 8) = uVar2;
      }
    }
    else if (param_3 == 2) {
      (*API_USER32_DLL_GetWindowLongA)(*(undefined4 *)(local_8 + 4),local_c);
      pcVar1 = (code *)FUN__text__0056ce80();
      if (pcVar1 != FUN__text__00424cc0) {
        (*API_USER32_DLL_SetWindowLongA)(*(undefined4 *)(local_8 + 4),local_c,FUN__text__00424cc0);
        uVar2 = FUN__text__0056ce80();
        *(undefined4 *)(local_8 + 8) = uVar2;
      }
    }
  }
  local_8 = 0x4248d3;
  FUN__text__0056ce80();
  return;
}

