
void FUN__text__0040a400(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  int *local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = FUN__text__00409f70(param_1,param_2);
  if ((*local_8 == 0) &&
     (iVar3 = FUN__text__00424f80("AnmData!=0",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                  DAT_005ff0f8 + 5,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (((param_2 < 0) || (3 < param_2)) &&
     (iVar3 = FUN__text__00424f80("(0<=off)&&(off<=3)",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                  DAT_005ff0f8 + 6,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (((param_3 < 0) || (*(int *)(local_c + 4) <= param_3)) &&
     (iVar3 = FUN__text__00424f80("(0<=no)&&(no<file->rcnt)",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                  DAT_005ff0f8 + 7,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (((*local_8 != 0) && (param_2 < 4)) && (param_3 < *(int *)(local_c + 4))) {
    uVar2 = FUN__text__004214f0(local_c,param_3);
    *(undefined4 *)(param_1 + 4) = uVar2;
    FUN__text__0040a520(param_1);
  }
  local_8 = (int *)0x40a50f;
  FUN__text__0056ce80();
  return;
}

