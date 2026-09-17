
void __thiscall FUN__text__0049d160(int param_1,short param_2,short param_3,short param_4)

{
  code *pcVar1;
  undefined2 extraout_var;
  int iVar2;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 uVar3;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined2 extraout_var_08;
  undefined2 extraout_var_09;
  undefined2 extraout_var_10;
  undefined4 *puVar4;
  undefined4 local_98 [16];
  uint local_58;
  int local_54;
  ushort local_50;
  ushort uStack_4e;
  ushort local_4c;
  undefined1 local_48;
  undefined1 uStack_47;
  byte bStack_46;
  byte bStack_45;
  byte local_44;
  uint local_24;
  short local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_98;
  for (iVar2 = 0x25; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (((*(short *)(param_1 + 0x30992) != -1) || (*(int *)(param_1 + 0x108b50) != 0)) &&
     (*(short *)(param_1 + 0x109d4e) != -1)) {
    local_c = param_1 + 0x80aec + *(short *)(param_1 + 0x109d4e) * 0x520;
    local_8 = param_1;
    iVar2 = FUN__text__00468d10(local_c);
    if (iVar2 != 0) {
      FUN__text__004deaa0(local_c,&local_50);
      iVar2 = FUN__text__0046a4c0(local_c);
      uVar3 = extraout_var_02;
      if (iVar2 != 0) {
        FUN__text__0046db20(local_c,1);
        uVar3 = extraout_var_03;
      }
      FUN__text__0046d340(local_c,(int)param_2,(int)param_3,CONCAT22(uVar3,param_4));
      local_1c = CONCAT22(local_1c._2_2_,param_4 + -1);
      local_54 = (0x5b - *(short *)(local_8 + 0xe0970 +
                                   (uint)*(ushort *)(*(int *)(local_c + 600) + 2) * 0x80)) / 2;
      if (local_54 < 0) {
        local_54 = 0;
      }
      *(short *)(local_8 + 0xe09a6 + (uint)*(ushort *)(*(int *)(local_c + 600) + 2) * 0x80) =
           param_4;
      FUN__text__00408f10(local_54 + 0x4f,0x26f,0xffffffff);
      FUN__text__00472b30(99,0x28b,local_1c & 0xffff,(int)*(short *)(*(int *)(local_c + 600) + 0x16)
                          ,3,0xffffffff);
      FUN__text__00472b30(0x82,0x28b,local_1c & 0xffff,
                          (int)*(short *)(*(int *)(local_c + 600) + 0x14),3,0xffffffff);
      FUN__text__00472b30(99,0x29e,local_1c & 0xffff,(int)*(short *)(*(int *)(local_c + 600) + 0x1c)
                          ,3,0xffffffff);
      FUN__text__00472b30(0x82,0x29e,local_1c & 0xffff,
                          (int)*(short *)(*(int *)(local_c + 600) + 0x1a),3,0xffffffff);
      *(short *)(local_8 + 0x1009a6 + (uint)*(byte *)(local_c + 0x14) * 0x80) = param_4;
      FUN__text__00408f10(0x54,0x2ca,0xffffffff);
      local_10 = (*(int *)(local_c + 0x1c) % 0x34bc0) / 0xe10;
      local_14 = (*(int *)(local_c + 0x1c) % 0xe10) / 0x3c;
      FUN__text__00472b30(0x87,0x2cc,CONCAT22((short)((uint)local_14 >> 0x10),(undefined2)local_1c),
                          local_10,0xfffffffe,0xfff66f6f);
      FUN__text__00472b30(0x9a,0x2cc,CONCAT22(extraout_var_04,(undefined2)local_1c),local_14,
                          0xfffffffe,0xfff66f6f);
      *(short *)(local_8 + 0x1009a6 + (uint)*(byte *)(local_c + 0x34) * 0x80) = param_4;
      FUN__text__00408f10(0x54,0x2dd,0xffffffff);
      local_10 = (*(int *)(local_c + 0x3c) % 0x34bc0) / 0xe10;
      local_14 = (*(int *)(local_c + 0x3c) % 0xe10) / 0x3c;
      FUN__text__00472b30(0x87,0x2df,CONCAT22((short)((uint)local_14 >> 0x10),(undefined2)local_1c),
                          local_10,0xfffffffe,0xff18ff00);
      FUN__text__00472b30(0x9a,0x2df,CONCAT22(extraout_var_05,(undefined2)local_1c),local_14,
                          0xfffffffe,0xff18ff00);
      *(short *)(local_8 + 0xf09a6 + (uint)*(ushort *)(*(int *)(local_c + 600) + 0xc) * 0x80) =
           param_4;
      FUN__text__00408f10(0xc4,0x26f,0xffffffff);
      if (*(ushort *)(*(int *)(local_c + 600) + 2) < 0x40) {
        FUN__text__00472b30(0x11a,0x271,local_1c & 0xffff,
                            *(undefined1 *)(*(int *)(local_c + 600) + 0xe),2,0xffffffff);
      }
      else {
        FUN__text__0040ec50(0x11d,0x26d,(local_1c & 0xffff) - 1,0xffffffff,0,&DAT_005a05a4);
      }
      iVar2 = (uint)*(ushort *)(*(int *)(local_c + 600) + 0xc) * 0x40;
      local_20 = *(short *)(&DAT_006b2da0 + iVar2);
      local_24 = CONCAT31(local_24._1_3_,(&DAT_006c2dcd)[local_20 * 0x48]);
      if ((&DAT_006c2dcd)[local_20 * 0x48] == '\x02') {
        *(short *)(local_8 + 0xdeaa6) = param_4;
        FUN__text__00408f10(0xd1,0x28a,0xffffffff);
      }
      else {
        local_18 = (uint)local_4c;
        FUN__text__00472b30(0xd3,0x28b,CONCAT22((short)((uint)iVar2 >> 0x10),(undefined2)local_1c),
                            local_18,3,0xffffffff);
      }
      local_58 = local_24 & 0xff;
      switch(local_58) {
      case 0:
      case 3:
        break;
      case 1:
      case 4:
        *(short *)(local_8 + 0xde9a6) = param_4;
        FUN__text__00408f10(0x10e,0x289,0xffffffff);
        break;
      case 2:
        *(short *)(local_8 + 0xdea26) = param_4;
        FUN__text__00408f10(0x10e,0x289,0xffffffff);
        break;
      default:
        iVar2 = FUN__text__00424f80(&DAT_005a0548,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlWindow.CPP",
                                    DAT_0061b004 + 0x97,0);
        if (iVar2 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
      local_18 = (uint)local_50;
      FUN__text__00472b30(0xd3,0x29e,local_1c & 0xffff,local_18,3,0xffffffff);
      local_18 = (uint)local_50 + (uint)uStack_4e;
      FUN__text__00472b30(0x106,0x29e,CONCAT22((short)(local_18 >> 0x10),(undefined2)local_1c),
                          local_18,3,0xffffffff);
      *(short *)(local_8 + 0x1009a6 + (uint)*(byte *)(*(int *)(local_c + 600) + 0x45) * 0x80) =
           param_4;
      FUN__text__00408f10(0xcf,0x2b0,0xffffffff);
      local_18 = (uint)*(byte *)(*(int *)(local_c + 600) + 0x37);
      FUN__text__00472b30(0xd3,0x2cc,
                          CONCAT22((short)((uint)*(int *)(local_c + 600) >> 0x10),
                                   (undefined2)local_1c),local_18,3,0xffffffff);
      FUN__text__00472b30(0xd3,0x2df,local_1c & 0xffff,
                          *(undefined1 *)(*(int *)(local_c + 600) + 0x44),3,0xffffffff);
      FUN__text__00472b30(0x10c,0x2df,local_1c & 0xffff,
                          *(undefined2 *)(*(int *)(local_c + 600) + 0x34),4,0xffffffff);
      iVar2 = FUN__text__0046a4c0(local_c);
      if ((iVar2 != 0) && (*(int *)(*(int *)(local_c + 600) + 0x24) != 0x7fffffff)) {
        iVar2 = *(int *)(*(int *)(local_c + 600) + 0x24);
        FUN__text__00472f40(0x157,0x271,
                            CONCAT22((short)((uint)(iVar2 % 0x3c) >> 0x10),(undefined2)local_1c),
                            iVar2 / 0x3c,1,0,0xffffffff,1);
      }
      local_18 = CONCAT12(bStack_46,CONCAT11(uStack_47,local_48)) & 0xff;
      FUN__text__00472b30(0x155,0x28b,local_1c & 0xffff,local_18,3,0xffffffff);
      local_18 = CONCAT12(bStack_45,CONCAT11(bStack_46,uStack_47)) & 0xff;
      FUN__text__00472b30(0x155,0x29d,CONCAT22(extraout_var_06,(undefined2)local_1c),local_18,3,
                          0xffffffff);
      local_18 = (uint)local_44;
      FUN__text__00472b30(0x150,0x2b1,CONCAT22(extraout_var_07,(undefined2)local_1c),local_18,3,
                          0xffffffff);
      local_18 = (uint)bStack_45;
      FUN__text__00472b30(0x155,0x2cc,CONCAT22(extraout_var_08,(undefined2)local_1c),local_18,3,
                          0xffffffff);
      local_18 = (uint)bStack_46;
      FUN__text__00472b30(0x150,0x2df,CONCAT22(extraout_var_09,(undefined2)local_1c),local_18,3,
                          0xffffffff);
      FUN__text__0049da20(local_c,0,0x9a,0x288,CONCAT22(extraout_var,(undefined2)local_1c));
      FUN__text__0049da20(local_c,1,0x9a,0x29b,CONCAT22(extraout_var_10,(undefined2)local_1c));
      FUN__text__0049d9e0(local_c,CONCAT22(extraout_var_00,(undefined2)local_1c));
    }
    iVar2 = FUN__text__0046a390(local_c);
    if (iVar2 != 0) {
      FUN__text__0040a330(local_8 + 0x1098a8,local_8 + 0xde4b0,(int)param_2,(int)param_3,
                          CONCAT22(extraout_var_01,param_4));
    }
  }
  local_8 = 0x49d9bb;
  FUN__text__0056ce80();
  return;
}

