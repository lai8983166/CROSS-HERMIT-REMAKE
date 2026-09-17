
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0055e470(uint *param_1,uint *param_2,uint *param_3)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  uint uVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  uint uVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  uint uVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  uint uVar21;
  uint uVar22;
  uint uVar23;
  uint uVar24;
  uint uVar25;
  uint uVar26;
  uint uVar27;
  uint uVar28;
  
  fVar6 = (float)(*param_1 & _DAT_00760460);
  fVar10 = (float)(param_1[1] & _UNK_00760464);
  fVar14 = (float)(param_1[2] & _UNK_00760468);
  fVar18 = (float)(param_1[3] & _UNK_0076046c);
  uVar22 = param_1[1] & _UNK_00760454;
  uVar23 = param_1[2] & _UNK_00760458;
  uVar24 = param_1[3] & _UNK_0076045c;
  fVar7 = fVar6 * _DAT_00760440 + _DAT_007603f0;
  fVar11 = fVar10 * _UNK_00760444 + _UNK_007603f4;
  fVar15 = fVar14 * _UNK_00760448 + _UNK_007603f8;
  fVar19 = fVar18 * _UNK_0076044c + _UNK_007603fc;
  fVar8 = fVar7 - _DAT_007603f0;
  fVar12 = fVar11 - _UNK_007603f4;
  fVar16 = fVar15 - _UNK_007603f8;
  fVar20 = fVar19 - _UNK_007603fc;
  fVar6 = (((fVar6 - _DAT_00760430 * fVar8) - _DAT_00760420 * fVar8) - _DAT_00760410 * fVar8) -
          _DAT_00760400 * fVar8;
  fVar8 = (((fVar10 - _UNK_00760434 * fVar12) - _UNK_00760424 * fVar12) - _UNK_00760414 * fVar12) -
          _UNK_00760404 * fVar12;
  fVar10 = (((fVar14 - _UNK_00760438 * fVar16) - _UNK_00760428 * fVar16) - _UNK_00760418 * fVar16) -
           _UNK_00760408 * fVar16;
  fVar12 = (((fVar18 - _UNK_0076043c * fVar20) - _UNK_0076042c * fVar20) - _UNK_0076041c * fVar20) -
           _UNK_0076040c * fVar20;
  fVar14 = fVar6 * fVar6;
  fVar16 = fVar8 * fVar8;
  fVar18 = fVar10 * fVar10;
  fVar20 = fVar12 * fVar12;
  uVar25 = (uint)fVar7 & (uint)PTR_DAT_007603c0;
  uVar26 = (uint)fVar11 & (uint)PTR_DAT_007603c4;
  uVar27 = (uint)fVar15 & (uint)PTR_DAT_007603c8;
  uVar28 = (uint)fVar19 & (uint)PTR_DAT_007603cc;
  uVar9 = uVar25 & _DAT_007603b0;
  uVar13 = uVar26 & _UNK_007603b4;
  uVar17 = uVar27 & _UNK_007603b8;
  uVar21 = uVar28 & _UNK_007603bc;
  uVar1 = uVar26 - uVar13 & _DAT_007603a0;
  uVar2 = uVar27 - uVar17 & _DAT_007603a0;
  uVar3 = uVar28 - uVar21 & _DAT_007603a0;
  uVar4 = uVar25 + uVar9 & _DAT_007603a0;
  uVar26 = uVar26 + uVar13 & _DAT_007603a0;
  uVar27 = uVar27 + uVar17 & _DAT_007603a0;
  uVar28 = uVar28 + uVar21 & _DAT_007603a0;
  uVar5 = -(uint)((float)(uVar9 << 0x1e) != 0.0);
  uVar13 = -(uint)((float)(uVar13 << 0x1e) != 0.0);
  uVar17 = -(uint)((float)(uVar17 << 0x1e) != 0.0);
  uVar21 = -(uint)((float)(uVar21 << 0x1e) != 0.0);
  fVar6 = (((_DAT_007603e0 * fVar14 + _DAT_00760390) * fVar14 + _DAT_00760370) * fVar14 +
          _DAT_00760350) * fVar6;
  fVar8 = (((_UNK_007603e4 * fVar16 + _UNK_00760394) * fVar16 + _UNK_00760374) * fVar16 +
          _UNK_00760354) * fVar8;
  fVar10 = (((_UNK_007603e8 * fVar18 + _UNK_00760398) * fVar18 + _UNK_00760378) * fVar18 +
           _UNK_00760358) * fVar10;
  fVar12 = (((_UNK_007603ec * fVar20 + _UNK_0076039c) * fVar20 + _UNK_0076037c) * fVar20 +
           _UNK_0076035c) * fVar12;
  fVar7 = (((_DAT_007603d0 * fVar14 + _DAT_00760380) * fVar14 + _DAT_00760360) * fVar14 +
          _DAT_00760340) * fVar14 + _DAT_00760330;
  fVar11 = (((_UNK_007603d4 * fVar16 + _UNK_00760384) * fVar16 + _UNK_00760364) * fVar16 +
           _UNK_00760344) * fVar16 + _UNK_00760334;
  fVar14 = (((_UNK_007603d8 * fVar18 + _UNK_00760388) * fVar18 + _UNK_00760368) * fVar18 +
           _UNK_00760348) * fVar18 + _UNK_00760338;
  fVar15 = (((_UNK_007603dc * fVar20 + _UNK_0076038c) * fVar20 + _UNK_0076036c) * fVar20 +
           _UNK_0076034c) * fVar20 + _UNK_0076033c;
  *param_2 = (~uVar5 & (uint)fVar6 | uVar5 & (uint)fVar7) ^
             (uVar25 - uVar9 & _DAT_007603a0) << 0x1e ^ *param_1 & _DAT_00760450;
  param_2[1] = (~uVar13 & (uint)fVar8 | uVar13 & (uint)fVar11) ^ uVar1 << 0x1e ^ uVar22;
  param_2[2] = (~uVar17 & (uint)fVar10 | uVar17 & (uint)fVar14) ^ uVar2 << 0x1e ^ uVar23;
  param_2[3] = (~uVar21 & (uint)fVar12 | uVar21 & (uint)fVar15) ^ uVar3 << 0x1e ^ uVar24;
  *param_3 = (uVar5 & (uint)fVar6 | ~uVar5 & (uint)fVar7) ^ uVar4 << 0x1e;
  param_3[1] = (uVar13 & (uint)fVar8 | ~uVar13 & (uint)fVar11) ^ uVar26 << 0x1e;
  param_3[2] = (uVar17 & (uint)fVar10 | ~uVar17 & (uint)fVar14) ^ uVar27 << 0x1e;
  param_3[3] = (uVar21 & (uint)fVar12 | ~uVar21 & (uint)fVar15) ^ uVar28 << 0x1e;
  return;
}

