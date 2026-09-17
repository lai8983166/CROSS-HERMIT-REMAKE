
void FUN__text__004163e0(int param_1,undefined4 param_2,undefined4 param_3,undefined2 param_4,
                        undefined4 param_5,undefined4 param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44c [16];
  int local_40c;
  undefined1 *local_408;
  undefined1 local_404 [1020];
  undefined4 uStack_8;
  
  puVar2 = local_44c;
  for (iVar1 = 0x112; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(short *)(param_1 + 0xb28e) != 0) && (*(int *)(param_1 + 0xb270) != 0)) &&
     (iVar1 = FUN__text__0040e2a0(param_2,param_3,0x200,0x80), iVar1 == 0)) {
    local_408 = &stack0x0000001c;
    FUN__text__0056dbb0(local_404,param_6,local_408);
    local_408 = (undefined1 *)0x0;
    local_40c = FUN__text__0040dcd0(2);
    *(undefined4 *)(local_40c + 4) = 2;
    *(undefined4 *)(local_40c + 8) = *(undefined4 *)(param_1 + 0xb270);
    *(undefined4 *)(local_40c + 0x10) = param_5;
    *(undefined2 *)(local_40c + 0xc) = (undefined2)param_2;
    *(undefined2 *)(local_40c + 0xe) = (undefined2)param_3;
    (*API_KERNEL32_DLL_lstrcpyA)(local_40c + 0x14,local_404);
    FUN__text__0056ce80();
    FUN__text__0040df20(local_40c,param_4);
  }
  uStack_8 = 0x416531;
  FUN__text__0056ce80();
  return;
}

