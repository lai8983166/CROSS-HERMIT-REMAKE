
void FUN__text__004496d0(undefined4 param_1,int *param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 local_78 [16];
  int *local_38;
  int *local_34;
  int *local_30;
  int local_2c;
  undefined4 local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f4ab;
  local_10 = ExceptionList;
  puVar4 = local_78;
  for (iVar3 = 0x1a; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00446290(param_2);
  local_24 = FUN__text__00428380();
  if (local_24 != 0) {
    local_2c = local_24;
    local_34 = (int *)FUN__text__00428a40(local_24 * 0x80 + 4);
    local_8 = 0;
    if (local_34 == (int *)0x0) {
      local_38 = (int *)0x0;
    }
    else {
      *local_34 = local_2c;
      _eh_vector_constructor_iterator_
                (local_34 + 1,0x80,local_2c,FUN__text__004075e0,FUN__text__00407710);
      local_38 = local_34 + 1;
    }
    local_30 = local_38;
    local_8 = 0xffffffff;
    param_2[1] = (int)local_38;
    if ((param_2[1] == 0) &&
       (iVar3 = FUN__text__00424f80("fm->sp!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                    DAT_00606750 + 0xc,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *param_2 = local_24;
    for (local_1c = 0; local_1c != local_24; local_1c = local_1c + 1) {
      local_18 = FUN__text__0044c0a0(param_3,local_1c);
      local_18 = local_18 + param_4;
      local_28 = FUN__text__0044c2c0(local_18);
      FUN__text__004077c0(DAT_007a49fc);
      uVar7 = 0;
      uVar5 = *(undefined4 *)(local_14 + 0x1ba0);
      uVar6 = local_28;
      uVar2 = FUN__text__004142b0(uVar5,local_28,0);
      local_20 = FUN__text__00408e30(uVar2,uVar5,uVar6,uVar7);
      if ((local_20 != 0) &&
         (iVar3 = FUN__text__00424f80(&DAT_00598390,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                      DAT_00606750 + 0x18,0), iVar3 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  ExceptionList = local_10;
  local_8 = 0x4498ac;
  FUN__text__0056ce80();
  return;
}

