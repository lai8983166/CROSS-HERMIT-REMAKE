
void __fastcall FUN__text__004be0b0(undefined4 param_1)

{
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 uVar1;
  int iVar2;
  short sVar3;
  undefined2 extraout_var_01;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  undefined2 local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar4 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar1 = 0xcccc;
  local_8 = param_1;
  for (local_10 = 0; local_10 < 5; local_10 = local_10 + 1) {
    local_14 = *(short *)(&DAT_007aaaae + local_10 * 2);
    if (local_14 < 0) {
      FUN__text__004d2620(1,local_10 * 0x8a + 0x27,0xc6,0x86,0x52,0xa0010101,1);
      uVar1 = extraout_var_00;
    }
    else {
      FUN__text__004be950(CONCAT22(local_14 >> 0xf,local_10),
                          CONCAT22(uVar1,*(undefined2 *)(&DAT_007a5262 + local_14 * 2)));
      uVar1 = extraout_var;
    }
  }
  local_18 = 0;
  for (local_10 = 0; local_10 < 5; local_10 = local_10 + 1) {
    for (local_c = 0; local_c < 4; local_c = local_c + 1) {
      local_14 = *(short *)(&DAT_007aaae0 + local_10 * 8 + local_c * 2);
      if (local_14 < 0) {
        FUN__text__004d2620(local_c * 0xc6 + 0xe7,local_10 * 0x8a + 0x27,0xc6,0x86,0x52,0xa0010101,1
                           );
      }
      else {
        local_18 = *(undefined2 *)(&DAT_007a5210 + local_14 * 2);
        sVar3 = local_14 >> 0xf;
        FUN__text__004be2e0(local_c,CONCAT22(local_c >> 0xf,local_10),CONCAT22(sVar3,local_18),
                            DAT_007e1190,CONCAT22(local_c >> 0xf,DAT_007e1196),
                            CONCAT22(sVar3,DAT_007e1194),CONCAT22(sVar3,DAT_007e1198));
      }
    }
  }
  FUN__text__004bef20(0x15e,0x2e2,0,0,9,0x57,DAT_007e119c,10,1,4,7,0,&DAT_0061c700,&DAT_0061c790);
  FUN__text__004d2700(&DAT_0061c610,1,0x59,0,0);
  FUN__text__004d2700(&DAT_0061c600,1,0x50,*(undefined2 *)(DAT_007a49fc + 0x196c),
                      CONCAT22(extraout_var_01,*(undefined2 *)(DAT_007a49fc + 0x1970)));
  local_8 = 0x4be2d2;
  FUN__text__0056ce80();
  return;
}

