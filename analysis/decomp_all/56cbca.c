
undefined4
FUN_0056cbca(char *param_1,undefined4 param_2,undefined4 param_3,char *param_4,int param_5)

{
  char cVar1;
  code *pcVar2;
  char *pcVar3;
  undefined4 uVar4;
  char *pcVar5;
  char *pcVar6;
  char *pcVar7;
  undefined4 uVar8;
  undefined1 local_cb8 [3000];
  char local_100 [200];
  char local_38 [52];
  
  FUN_0056d810(local_38,&PTR_DAT_005f9380,param_2);
  pcVar2 = API_KERNEL32_DLL_OutputDebugStringA;
  if (param_1 != (char *)0x0) {
    pcVar3 = param_1;
    do {
      cVar1 = *pcVar3;
      pcVar3 = pcVar3 + 1;
    } while (cVar1 != '\0');
    if (pcVar3 + (200 - (int)(param_1 + 1)) < (char *)0xbb8) {
      FUN_0056d810(local_cb8,"%s(%s): ",param_1,local_38);
      (*pcVar2)(local_cb8);
    }
  }
  if (param_4 != (char *)0x0) {
    (*pcVar2)(param_4);
  }
  uVar8 = param_3;
  uVar4 = FUN_00562570(param_3);
  FUN_0056d810(local_100,"%s (0x%0.8x)",uVar4,uVar8);
  FUN_0056d810(local_cb8," (hr=%s)",local_100);
  (*pcVar2)(local_cb8);
  (*pcVar2)(&DAT_005f9354);
  if (param_5 != 0) {
    pcVar3 = param_4;
    do {
      cVar1 = *pcVar3;
      pcVar3 = pcVar3 + 1;
    } while (cVar1 != '\0');
    pcVar5 = param_1;
    do {
      cVar1 = *pcVar5;
      pcVar5 = pcVar5 + 1;
    } while (cVar1 != '\0');
    pcVar6 = local_38;
    do {
      cVar1 = *pcVar6;
      pcVar6 = pcVar6 + 1;
    } while (cVar1 != '\0');
    pcVar7 = local_100;
    do {
      cVar1 = *pcVar7;
      pcVar7 = pcVar7 + 1;
    } while (cVar1 != '\0');
    if (pcVar7 + (int)&stack0x00000000 * -2 + (int)pcVar6 +
        (int)(pcVar3 + (int)(pcVar5 + ((0x1fe - (int)(param_1 + 1)) - (int)(param_4 + 1)))) <
        (char *)0xbb8) {
      FUN_0056d810(local_cb8,"File: %s\nLine: %s\nError Code: %s\nCalling: %s",param_1,local_38,
                   local_100,param_4);
      (*DAT_005923d8)(0,local_cb8,"Unexpected error encountered",0x10);
    }
  }
  return param_3;
}

