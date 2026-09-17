
void FUN__text__00445f60(undefined4 param_1,int *param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined1 *puVar6;
  undefined4 uVar7;
  undefined4 local_278 [16];
  int *local_238;
  int *local_234;
  int *local_230;
  int local_22c;
  undefined1 local_228 [512];
  undefined1 *local_28;
  int local_24;
  int local_20;
  int local_1c;
  int *local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f48e;
  local_10 = ExceptionList;
  puVar4 = local_278;
  for (iVar3 = 0x9a; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00446290(param_2);
  local_24 = FUN__text__00428380();
  if (local_24 != 0) {
    local_22c = local_24;
    local_234 = (int *)FUN__text__00428a40(local_24 * 0x80 + 4);
    local_8 = 0;
    if (local_234 == (int *)0x0) {
      local_238 = (int *)0x0;
    }
    else {
      *local_234 = local_22c;
      _eh_vector_constructor_iterator_
                (local_234 + 1,0x80,local_22c,FUN__text__004075e0,FUN__text__00407710);
      local_238 = local_234 + 1;
    }
    local_230 = local_238;
    local_8 = 0xffffffff;
    param_2[1] = (int)local_238;
    if ((param_2[1] == 0) &&
       (iVar3 = FUN__text__00424f80("fm->sp!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                    DAT_00606724 + 0xe,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *param_2 = local_24;
    local_18 = (int *)FUN__text__00418780();
    for (local_1c = 0; local_1c != local_24; local_1c = local_1c + 1) {
      if ((*local_18 <= local_1c) &&
         (iVar3 = FUN__text__00424f80("i < se->cnt",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_00606724 + 0x18,0), iVar3 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      FUN__text__0056d810(local_228,"%s(Ver:%d.%d)",local_18[local_1c * 0x15 + 0xf],
                          (uint)local_18[local_1c * 0x15 + 0x13] >> 0x10,
                          (short)local_18[local_1c * 0x15 + 0x13]);
      local_28 = local_228;
      FUN__text__004077c0(DAT_007a49fc);
      uVar7 = 0;
      uVar5 = *(undefined4 *)(local_14 + 0x1ba0);
      puVar6 = local_28;
      uVar2 = FUN__text__004142b0(uVar5,local_28,0);
      local_20 = FUN__text__00408e30(uVar2,uVar5,puVar6,uVar7);
      if ((local_20 != 0) &&
         (iVar3 = FUN__text__00424f80(&DAT_00598390,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_00606724 + 0x1f,0), iVar3 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  ExceptionList = local_10;
  local_8 = 0x4461e5;
  FUN__text__0056ce80();
  return;
}

