
void __fastcall FUN__text__00466000(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  undefined4 local_28;
  int local_24;
  undefined4 local_20;
  int local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0059009b;
  local_10 = ExceptionList;
  puVar3 = local_68;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  local_14 = param_1;
  if (*(int *)(param_1 + 0x2a6e8) != 0) {
    ExceptionList = &local_10;
    iVar2 = FUN__text__00424f80("UnitEfctTbl[0] == 0",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",DAT_00618b18 + 3
                                ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_24 = FUN__text__00428a40(0x54);
  local_8 = 0;
  if (local_24 == 0) {
    local_28 = 0;
  }
  else {
    local_28 = FUN__text__00464c60();
  }
  local_20 = local_28;
  local_8 = 0xffffffff;
  *(undefined4 *)(local_14 + 0x2a6e8) = local_28;
  if (*(int *)(local_14 + 0x2a6e8) == 0) {
    iVar2 = FUN__text__00424f80("UnitEfctTbl[0]!=0",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",DAT_00618b18 + 5
                                ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_1c = FUN__text__00464d70(DAT_007a49fc,0);
  *(undefined4 *)(*(int *)(local_14 + 0x2a6e8) + 0x28) = 100;
  local_1c = FUN__text__00464de0("data\\DxAnim\\Efct.bin",0,1);
  if (local_1c != 0) {
    iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618b18 + 0xb,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  FUN__text__0040b960(1);
  _memset((void *)(local_14 + 0x109340),0,0x3340);
  for (local_18 = 0; local_18 != 10; local_18 = local_18 + 1) {
    *(undefined2 *)(local_14 + 0x109340 + local_18 * 0x520) = 1;
    *(undefined4 *)(local_14 + 0x109384 + local_18 * 0x520) = *(undefined4 *)(local_14 + 0x2a6e8);
    FUN__text__00409ef0(local_14 + 0x109388 + local_18 * 0x520);
  }
  *(undefined4 *)(local_14 + 0x109384) = *(undefined4 *)(local_14 + 0x2a6e8);
  FUN__text__00409ef0(local_14 + 0x109388);
  FUN__text__00409ff0(local_14 + 0x109388,1,0x41,0);
  *(undefined4 *)(local_14 + 0x109dc4) = *(undefined4 *)(local_14 + 0x2a6e8);
  FUN__text__00409ef0(local_14 + 0x109dc8);
  *(undefined4 *)(local_14 + 0x10a2e4) = *(undefined4 *)(local_14 + 0x2a6e8);
  FUN__text__00409ef0(local_14 + 0x10a2e8);
  FUN__text__00466500();
  FUN__text__004937a0();
  ExceptionList = local_10;
  local_8 = 0x4662ac;
  FUN__text__0056ce80();
  return;
}

