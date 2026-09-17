
void __fastcall FUN__text__004ce8f0(int param_1)

{
  uint uVar1;
  undefined1 uVar2;
  char cVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_74 [16];
  int local_34;
  int local_30;
  uint local_2c;
  char local_28;
  undefined3 uStack_27;
  uint local_24;
  uint local_20;
  uint local_1c;
  uint local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined2 *local_c;
  int local_8;
  
  puVar5 = local_74;
  for (iVar4 = 0x1c; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_14 = 0;
  local_18 = local_18 & 0xffff0000;
  DAT_007e100a = 0;
  local_8 = param_1;
  if ((*(char *)(param_1 + 4) != '\0') && (local_14 = 1, *(char *)(param_1 + 0x93e2) == '\0')) {
    local_c = (undefined2 *)(*(int *)(param_1 + 0x10) + *(int *)(param_1 + 0x1c));
    local_2c = (uint)*(ushort *)(param_1 + 0x20);
    switch(local_2c) {
    case 0:
      *(undefined2 *)(param_1 + 0x22) = *local_c;
      *(undefined2 *)(param_1 + 0x24) = local_c[1];
      if (*(short *)(param_1 + 0x22) == 0x13) {
        local_14 = 0;
        FUN__text__004ce090(0);
        FUN__text__004ce800();
      }
      else {
        DAT_007a4e18 = DAT_007a4e18 + 1;
        DAT_007a4e1c = 0;
        local_30 = *(ushort *)(param_1 + 0x22) - 5;
        switch(local_30) {
        case 0:
          local_10 = FUN__text__004c3f40(0,local_c,0);
          break;
        case 1:
          local_10 = FUN__text__004c4000(0,local_c,0);
          break;
        case 2:
          local_10 = FUN__text__004c4130(0,local_c,0);
          break;
        case 3:
          local_10 = FUN__text__004c23f0(0,local_c,0);
          break;
        case 4:
          local_10 = FUN__text__004c2500(0,local_c,0);
          break;
        case 6:
          local_10 = FUN__text__004c2610(0,local_c,0);
          break;
        case 7:
          local_10 = FUN__text__004c2670(0,local_c,1);
          break;
        case 8:
          local_10 = FUN__text__004c2730(0,local_c,1);
          break;
        case 9:
          local_10 = FUN__text__004c27f0(0,local_c,1);
          break;
        case 10:
          local_10 = FUN__text__004c21f0(0,local_c,2);
          break;
        case 0xb:
          local_10 = FUN__text__004c2370(0,local_c,2);
          break;
        case 0xc:
          local_10 = FUN__text__004c4b80(0,local_c,0);
          break;
        case 0xd:
          local_10 = FUN__text__004c4b40(0,local_c,0);
          break;
        case 0xf:
          local_10 = FUN__text__004c5500(0,local_c,0);
          break;
        case 0x10:
          local_10 = FUN__text__004c5590(0,local_c,0);
          break;
        case 0x11:
          local_10 = FUN__text__004c59a0(0,local_c,0);
          break;
        case 0x12:
          local_10 = FUN__text__004c5ab0(0,local_c,1);
          break;
        case 0x13:
          local_10 = FUN__text__004c5bc0(0,local_c,3);
          break;
        case 0x14:
          local_10 = FUN__text__004c5d00(0,local_c,1);
          break;
        case 0x15:
          local_10 = FUN__text__004c5d40(0,local_c,0);
          break;
        case 0x16:
          local_10 = FUN__text__004c5ea0(0,local_c,1);
          break;
        case 0x17:
          local_10 = FUN__text__004c5fc0(0,local_c,1);
          break;
        case 0x18:
          local_10 = FUN__text__004c6050(0,local_c,0);
          break;
        case 0x19:
          local_10 = FUN__text__004c61c0(0,local_c,1);
          break;
        case 0x1a:
          local_10 = FUN__text__004c6330(0,local_c,0);
          break;
        case 0x1b:
          local_10 = FUN__text__004c6400(0,local_c,1);
          break;
        case 0x1c:
          local_10 = FUN__text__004c64d0(0,local_c,0);
          break;
        case 0x1d:
          local_10 = FUN__text__004c65d0(0,local_c,1);
          break;
        case 0x1e:
          local_10 = FUN__text__004c66e0(0,local_c,3);
          break;
        case 0x1f:
          local_10 = FUN__text__004c6820(0,local_c,1);
          break;
        case 0x20:
          local_10 = FUN__text__004c6860(0,local_c,0);
          break;
        case 0x21:
          local_10 = FUN__text__004c6920(0,local_c,1);
          break;
        case 0x22:
          local_10 = FUN__text__004c69e0(0,local_c,0);
          break;
        case 0x23:
          local_10 = FUN__text__004c6aa0(0,local_c,1);
          break;
        case 0x24:
          local_10 = FUN__text__004c6b60(0,local_c,1);
          break;
        case 0x25:
          local_10 = FUN__text__004c6c70(0,local_c,1);
          break;
        case 0x26:
          local_10 = FUN__text__004c4dc0(0,local_c,0);
          break;
        case 0x27:
          local_10 = FUN__text__004c4eb0(0,local_c,0);
          break;
        case 0x28:
          local_10 = FUN__text__004c4f30(0,local_c,0);
          break;
        case 0x29:
          local_10 = FUN__text__004c4ff0(0,local_c,0);
          break;
        case 0x2a:
          local_10 = FUN__text__004c50b0(0,local_c,0);
          break;
        case 0x2b:
          local_10 = FUN__text__004c51a0(0,local_c,0);
          break;
        case 0x2c:
          local_10 = FUN__text__004c5220(0,local_c,1);
          break;
        case 0x2d:
          local_10 = FUN__text__004c5260(0,local_c,1);
          break;
        case 0x2e:
          local_10 = FUN__text__004c4210(0,local_c,1);
          break;
        case 0x2f:
          local_10 = FUN__text__004c4280(0,local_c,1);
          break;
        case 0x32:
          local_10 = FUN__text__004c53a0(0,local_c,0);
          break;
        case 0x33:
          local_10 = FUN__text__004c5430(0,local_c,1);
          break;
        case 0x34:
          local_10 = FUN__text__004c54c0(0,local_c,1);
          break;
        case 0x35:
          local_10 = FUN__text__004c56c0(0,local_c,0);
          break;
        case 0x36:
          local_10 = FUN__text__004c5810(0,local_c,1);
          break;
        case 0x37:
          local_10 = FUN__text__004c5960(0,local_c,1);
          break;
        case 0x38:
          local_10 = FUN__text__004c52a0(0,local_c,1);
          break;
        case 0x3a:
          local_10 = FUN__text__004c44d0(0,local_c,1);
          break;
        case 0x3b:
          local_10 = FUN__text__004c4570(0,local_c,1);
          break;
        case 0x3c:
          local_10 = FUN__text__004c45c0(0,local_c,0);
          break;
        case 0x3d:
          local_10 = FUN__text__004c46f0(0,local_c,0);
          break;
        case 0x3e:
          local_10 = FUN__text__004c28b0(0,local_c,0);
          break;
        case 0x3f:
          local_10 = FUN__text__004c2950(0,local_c,0);
          break;
        case 0x40:
          local_10 = FUN__text__004c2af0(0,local_c,0);
          break;
        case 0x41:
          local_10 = FUN__text__004c2d80(0,local_c,0);
          break;
        case 0x42:
          local_10 = FUN__text__004c3080(0,local_c,0);
          break;
        case 0x43:
          local_10 = FUN__text__004c3400(0,local_c,0);
          break;
        case 0x44:
          local_10 = FUN__text__004c3690(0,local_c,0);
          break;
        case 0x45:
          local_10 = FUN__text__004c3730(0,local_c,0);
          break;
        case 0x46:
          local_10 = FUN__text__004c37b0(0,local_c,0);
          break;
        case 0x47:
          local_10 = FUN__text__004c3890(0,local_c,0);
          break;
        case 0x48:
          local_10 = FUN__text__004c3970(0,local_c,0);
          break;
        case 0x49:
          local_10 = FUN__text__004c3a80(0,local_c,0);
          break;
        case 0x4a:
          local_10 = FUN__text__004c3b90(0,local_c,0);
          break;
        case 0x4b:
          local_10 = FUN__text__004c3ce0(0,local_c,0);
          break;
        case 0x4c:
          local_10 = FUN__text__004c3dc0(0,local_c,0);
          break;
        case 0x4d:
          local_10 = FUN__text__004d0a10(0,local_c,0);
          break;
        case 0x4e:
          local_10 = FUN__text__004d0a50(0,local_c,0);
          break;
        case 0x4f:
          local_10 = FUN__text__004d0a90(0,local_c,0);
          break;
        case 0x50:
          local_10 = FUN__text__004d0ad0(0,local_c,0);
          break;
        case 0x51:
          local_10 = FUN__text__004d11f0(0,local_c,0);
          break;
        case 0x52:
          local_10 = FUN__text__004d1260(0,local_c,0);
          break;
        case 0x53:
          local_10 = FUN__text__004d0b10(0,local_c,0);
          break;
        case 0x54:
          local_10 = FUN__text__004d0bb0(0,local_c,0);
          break;
        case 0x55:
          local_10 = FUN__text__004d0c80(0,local_c,0);
          break;
        case 0x56:
          local_10 = FUN__text__004d0da0(0,local_c,0);
          break;
        case 0x57:
          local_10 = FUN__text__0042c460(0,local_c,0);
          break;
        case 0x58:
          local_10 = FUN__text__0042c510(0,local_c,0);
          break;
        case 0x59:
          local_10 = FUN__text__0042c5c0(0,local_c,0);
          break;
        case 0x5a:
          local_10 = FUN__text__0042c670(0,local_c,0);
          break;
        case 0x5b:
          local_10 = FUN__text__0042c720(0,local_c,0);
          break;
        case 0x5c:
          local_10 = FUN__text__0042c7e0(0,local_c,0);
          break;
        case 0x5d:
          local_10 = FUN__text__0042c8a0(0,local_c,0);
          break;
        case 0x5e:
          local_10 = FUN__text__0042c960(0,local_c,0);
          break;
        case 0x5f:
          local_10 = FUN__text__0042ca20(0,local_c,0);
          break;
        case 0x60:
          local_10 = FUN__text__0042cb10(0,local_c,0);
          break;
        case 0x61:
          local_10 = FUN__text__0042cc00(0,local_c,0);
          break;
        case 0x62:
          local_10 = FUN__text__0042ccf0(0,local_c,0);
          break;
        case 99:
          local_10 = FUN__text__0042cde0(0,local_c,0);
          break;
        case 100:
          local_10 = FUN__text__0042ced0(0,local_c,0);
          break;
        case 0x65:
          local_10 = FUN__text__0042cfc0(0,local_c,0);
          break;
        case 0x66:
          local_10 = FUN__text__0042d0b0(0,local_c,0);
          break;
        case 0x67:
          local_10 = FUN__text__0042d1a0(0,local_c,0);
          break;
        case 0x68:
          local_10 = FUN__text__0042d2a0(0,local_c,0);
          break;
        case 0x69:
          local_10 = FUN__text__0042d3c0(0,local_c,0);
          break;
        case 0x6a:
          local_10 = FUN__text__0042dc00(0,local_c,0);
          break;
        case 0x6b:
          local_10 = FUN__text__0042dcf0(0,local_c,0);
          break;
        case 0x6c:
          local_10 = FUN__text__0042d460(0,local_c,0);
          break;
        case 0x6d:
          local_10 = FUN__text__0042d520(0,local_c,0);
          break;
        case 0x6e:
          local_10 = FUN__text__0042d5e0(0,local_c,0);
          break;
        case 0x6f:
          local_10 = FUN__text__0042d870(0,local_c,0);
          break;
        case 0x70:
          local_10 = FUN__text__0042d960(0,local_c,4);
          break;
        case 0x71:
          local_10 = FUN__text__0042d9f0(0,local_c,4);
          break;
        case 0x72:
          local_10 = FUN__text__0042da80(0,local_c,4);
          break;
        case 0x73:
          local_10 = FUN__text__0042dac0(0,local_c,4);
          break;
        case 0x74:
          local_10 = FUN__text__0042dbc0(0,local_c,4);
          break;
        case 0x75:
          local_10 = FUN__text__0042dde0(0,local_c,0);
          break;
        case 0x76:
          local_10 = FUN__text__0042de60(0,local_c,0);
          break;
        case 0x77:
          local_10 = FUN__text__0042dee0(0,local_c,0);
          break;
        case 0x78:
          local_10 = FUN__text__0042e010(0,local_c,0);
          break;
        case 0x79:
          local_10 = FUN__text__0042d6d0(0,local_c,0);
          break;
        case 0x7a:
          local_10 = FUN__text__0042d7b0(0,local_c,0);
          break;
        case 0x7b:
          local_10 = FUN__text__0042e140(0,local_c,0);
          break;
        case 0x7c:
          local_10 = FUN__text__0042e240(0,local_c,0);
          break;
        case 0x7d:
          local_10 = FUN__text__0042e340(0,local_c,0);
          break;
        case 0x7e:
          local_10 = FUN__text__0042e470(0,local_c,0);
          break;
        case 0x7f:
          local_10 = FUN__text__0042e570(0,local_c,0);
          break;
        case 0x80:
          local_10 = FUN__text__0042e6c0(0,local_c,0);
          break;
        case 0x81:
          local_10 = FUN__text__0042e810(0,local_c,0);
          break;
        case 0x82:
          local_10 = FUN__text__0042e910(0,local_c,0);
          break;
        case 0x83:
          local_10 = FUN__text__0042e9e0(0,local_c,4);
          break;
        case 0x84:
          local_10 = FUN__text__0042ebc0(0,local_c,0);
          break;
        case 0x85:
          local_10 = FUN__text__0042ed90(0,local_c,0);
          break;
        case 0x86:
          local_10 = FUN__text__0042eef0(0,local_c,0);
          break;
        case 0x87:
          local_10 = FUN__text__0042f020(0,local_c,0);
          break;
        case 0x88:
          local_10 = FUN__text__0042f0a0(0,local_c,0);
          break;
        case 0x89:
          local_10 = FUN__text__0042f120(0,local_c,4);
          break;
        case 0x8a:
          local_10 = FUN__text__0042f1e0(0,local_c,0);
          break;
        case 0x8b:
          local_10 = FUN__text__004d0900(0,local_c,0);
          break;
        case 0x8c:
          local_10 = FUN__text__004d0990(0,local_c,0);
          break;
        case 0x8d:
          local_10 = FUN__text__0042f2d0(0,local_c,0);
          break;
        case 0x8e:
          local_10 = FUN__text__004d0ed0(0,local_c,0);
          break;
        case 0x8f:
          local_10 = FUN__text__004d0fb0(0,local_c,0);
          break;
        case 0x90:
          local_10 = FUN__text__004d1060(0,local_c,0);
          break;
        case 0x91:
          local_10 = FUN__text__004d1110(0,local_c,0);
          break;
        case 0x92:
          local_10 = FUN__text__004c4750(0,local_c,0);
          break;
        case 0x93:
          local_10 = FUN__text__004c4840(0,local_c,0);
          break;
        case 0x94:
          local_10 = FUN__text__004c4950(0,local_c,0);
          break;
        case 0x95:
          local_10 = FUN__text__004c4a60(0,local_c,0);
          break;
        case 0x96:
          local_10 = FUN__text__004c4af0(0,local_c,0);
          break;
        case 0x97:
          local_10 = FUN__text__004d12d0(0,local_c,0);
          break;
        case 0x98:
          local_10 = FUN__text__004d1360(0,local_c,0);
          break;
        case 0x99:
          local_10 = FUN__text__0042f460(0,local_c,0);
          break;
        case 0x9a:
          local_10 = FUN__text__0042f550(0,local_c,0);
          break;
        case 0x9b:
          local_10 = FUN__text__0042f640(0,local_c,0);
          break;
        case 0x9c:
          local_10 = FUN__text__0042f730(0,local_c,0);
          break;
        case 0x9d:
          local_10 = FUN__text__0042f820(0,local_c,0);
          break;
        case 0x9e:
          local_10 = FUN__text__0042f910(0,local_c,0);
          break;
        case 0x9f:
          local_10 = FUN__text__0042fa00(0,local_c,0);
          break;
        case 0xa0:
          local_10 = FUN__text__0042faf0(0,local_c,0);
          break;
        case 0xa1:
          local_10 = FUN__text__0042fbe0(0,local_c,0);
          break;
        case 0xa2:
          local_10 = FUN__text__0042fc60(0,local_c,0);
          break;
        case 0xa3:
          local_10 = FUN__text__004c43e0(0,local_c,1);
          break;
        case 0xa4:
          local_10 = FUN__text__004d13f0(0,local_c,0);
          break;
        case 0xa5:
          local_10 = FUN__text__004d14a0(0,local_c,0);
          break;
        case 0xa6:
          local_10 = FUN__text__004d1560(0,local_c,0);
          break;
        case 0xa7:
          local_10 = FUN__text__004c22b0(0,local_c,2);
        }
        *(uint *)(local_8 + 0x1c + (local_18 & 0xffff) * 0x1c8) =
             *(int *)(local_8 + 0x1c + (local_18 & 0xffff) * 0x1c8) +
             (uint)*(ushort *)(local_8 + 0x24 + (local_18 & 0xffff) * 0x1c8);
        *(undefined2 *)(local_8 + 0x20 + (local_18 & 0xffff) * 0x1c8) = (undefined2)local_10;
      }
      break;
    case 1:
      DAT_007a4e18 = 0;
      DAT_007a4e1c = DAT_007a4e1c + 1;
      local_20 = local_20 & 0xffffff00;
      local_34 = *(ushort *)(param_1 + 0x22) - 0xc;
      switch(*(ushort *)(param_1 + 0x22)) {
      case 0xc:
      case 0xd:
      case 0xe:
        uVar2 = FUN__text__004ccb90(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x17:
      case 0x1e:
      case 0x20:
        uVar2 = FUN__text__004cd060(0);
        local_24 = CONCAT31(local_24._1_3_,uVar2);
        cVar3 = FUN__text__004cd120(local_18 & 0xffff);
        _local_28 = CONCAT31(uStack_27,cVar3);
        uVar1 = local_20 >> 8;
        local_20 = local_20 & 0xffffff00;
        if (((local_24 & 0xff) == 1) && (cVar3 == '\x01')) {
          local_20 = CONCAT31((int3)uVar1,1);
        }
        break;
      case 0x18:
      case 0x19:
      case 0x1b:
      case 0x1c:
        uVar2 = FUN__text__004cd060(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x22:
      case 0x23:
      case 0x24:
      case 0x26:
      case 0x28:
      case 0x29:
      case 0x2a:
        uVar2 = FUN__text__004cd120(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x31:
        uVar2 = FUN__text__004cd2a0(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x32:
        uVar2 = FUN__text__004cd350(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x33:
        uVar2 = FUN__text__004cce20(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x34:
        uVar2 = FUN__text__004c8f60(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x38:
      case 0x39:
        uVar2 = FUN__text__004c7ab0();
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x3b:
      case 0x3c:
        uVar2 = FUN__text__004cd1e0(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x3d:
        uVar2 = FUN__text__004c8290(0);
        local_20 = CONCAT31(local_20._1_3_,uVar2);
        break;
      case 0x3f:
        iVar4 = FUN__text__004db270();
        if (iVar4 == 0) {
          local_20 = local_20 & 0xffffff00;
        }
        else {
          FUN__text__004db010((int)*(short *)(local_8 + 0x92d8));
          local_20 = CONCAT31(local_20._1_3_,1);
        }
        break;
      case 0x40:
      case 0x97:
        iVar4 = FUN__text__004db270();
        if (iVar4 == 0) {
          local_20 = local_20 & 0xffffff00;
        }
        else {
          FUN__text__004db120();
          local_20 = CONCAT31(local_20._1_3_,1);
        }
        break;
      case 0xa8:
        if (DAT_007f4491 == '\0') {
          uVar2 = FUN__text__004cce20(0);
          local_20 = CONCAT31(local_20._1_3_,uVar2);
        }
        else {
          uVar2 = FUN__text__004ccb90(0);
          local_20 = CONCAT31(local_20._1_3_,uVar2);
        }
      }
      if ((local_20 & 0xff) == 1) {
        *(undefined2 *)(local_8 + 0x20 + (local_18 & 0xffff) * 0x1c8) = 0;
      }
      break;
    case 2:
      *(undefined2 *)(param_1 + 0x20) = 0;
      break;
    case 4:
      if (*(char *)(param_1 + 0x92e0) == '\0') {
        *(undefined2 *)(param_1 + 0x20) = 0;
      }
      break;
    case 5:
    }
  }
  if (*(char *)(local_8 + 0x92e1) == '\0') {
    FUN__text__004d29e0(0x14,0,1,0x33,*(undefined2 *)(DAT_007a49fc + 0x196c),
                        *(undefined2 *)(DAT_007a49fc + 0x1970),0x1a8,0x18,0x14,0x1e,100,100,0xff,
                        0x80,0x80,0x80);
    local_1c = local_1c & 0xffff0000;
    while ((local_1c & 0xffff) < 10) {
      FUN__text__004ca1b0();
      FUN__text__004c99e0();
      FUN__text__004cd4d0(local_8 + 0x6f60 + (local_1c & 0xffff) * 0xe0,
                          local_8 + 0x430 + (local_1c & 0xffff) * 0xab8);
      local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
    }
    local_1c = local_1c & 0xffff0000;
    while ((local_1c & 0xffff) < 5) {
      if (*(char *)(local_8 + 0x1cf + (local_1c & 0xffff) * 0x12) != '\0') {
        FUN__text__004c7190();
      }
      local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
    }
    FUN__text__004c7770();
    local_1c = local_1c & 0xffff0000;
    while ((local_1c & 0xffff) < 0x14) {
      FUN__text__004cba60();
      local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
    }
  }
  local_8 = 0x4d03b3;
  FUN__text__0056ce80();
  return;
}

