
void __thiscall FUN__text__0042c380(int *param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    if (param_2 == 0) {
      (*API_WINMM_DLL_PlaySound)(*param_1,0,0x2005);
      FUN__text__0056ce80();
    }
    else {
      (*API_WINMM_DLL_PlaySound)(*param_1,0,0xd);
      FUN__text__0056ce80();
    }
  }
  local_8 = (int *)0x42c3f8;
  FUN__text__0056ce80();
  return;
}

