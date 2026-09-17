
uint FUN__text__00581730(int param_1)

{
  undefined2 uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  uint uVar15;
  uint uVar16;
  
  uVar1 = DAT_0080a658;
  if (param_1 == 0) {
    uVar2 = 0xffffffff;
  }
  else {
    uVar3 = FUN__text__0058aa30(1,DAT_0080a658,0x15,param_1 + 0xc);
    uVar4 = FUN__text__0058aa30(1,uVar1,0x14,param_1 + 0x10);
    uVar5 = FUN__text__0058aa30(1,uVar1,0x16,param_1 + 0x14);
    uVar6 = FUN__text__0058aa30(1,uVar1,0x17,param_1 + 0x18);
    uVar7 = FUN__text__0058aa30(1,uVar1,0x18,param_1 + 0x1c);
    fix_grouping(*(undefined4 *)(param_1 + 0x1c));
    uVar8 = FUN__text__0058aa30(1,uVar1,0x50,param_1 + 0x20);
    uVar9 = FUN__text__0058aa30(1,uVar1,0x51,param_1 + 0x24);
    uVar10 = FUN__text__0058aa30(0,uVar1,0x1a,param_1 + 0x28);
    uVar11 = FUN__text__0058aa30(0,uVar1,0x19,param_1 + 0x29);
    uVar12 = FUN__text__0058aa30(0,uVar1,0x54,param_1 + 0x2a);
    uVar13 = FUN__text__0058aa30(0,uVar1,0x55,param_1 + 0x2b);
    uVar14 = FUN__text__0058aa30(0,uVar1,0x56,param_1 + 0x2c);
    uVar15 = FUN__text__0058aa30(0,uVar1,0x57,param_1 + 0x2d);
    uVar16 = FUN__text__0058aa30(0,uVar1,0x52,param_1 + 0x2e);
    uVar2 = FUN__text__0058aa30(0,uVar1,0x53,param_1 + 0x2f);
    uVar2 = uVar3 | uVar4 | uVar5 | uVar6 | uVar7 | uVar8 | uVar9 | uVar10 | uVar11 | uVar12 |
            uVar13 | uVar14 | uVar15 | uVar16 | uVar2;
  }
  return uVar2;
}

