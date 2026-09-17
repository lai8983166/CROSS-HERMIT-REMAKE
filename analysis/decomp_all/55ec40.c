
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0055ec40(uint *param_1,uint *param_2,uint *param_3)

{
  float fVar1;
  float fVar2;
  uint uVar3;
  float fVar4;
  float fVar5;
  uint uVar6;
  float fVar7;
  float fVar8;
  uint uVar9;
  float fVar10;
  float fVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  uint uVar15;
  float fVar16;
  float fVar17;
  uint uVar18;
  uint uVar19;
  uint uVar20;
  uint uVar21;
  uint uVar22;
  uint uVar23;
  uint uVar24;
  float fVar25;
  float fVar26;
  uint uVar27;
  uint uVar28;
  
  fVar16 = (float)(*param_1 & _DAT_00760680);
  fVar17 = (float)(param_1[1] & _UNK_00760684);
  fVar25 = (float)(param_1[2] & _UNK_00760688);
  fVar26 = (float)(param_1[3] & _UNK_0076068c);
  uVar13 = param_1[1] & _UNK_00760674;
  uVar14 = param_1[2] & _UNK_00760678;
  uVar15 = param_1[3] & _UNK_0076067c;
  fVar1 = fVar16 * _DAT_00760660 + _DAT_00760610;
  fVar4 = fVar17 * _UNK_00760664 + _UNK_00760614;
  fVar7 = fVar25 * _UNK_00760668 + _UNK_00760618;
  fVar10 = fVar26 * _UNK_0076066c + _UNK_0076061c;
  fVar2 = fVar1 - _DAT_00760610;
  fVar5 = fVar4 - _UNK_00760614;
  fVar8 = fVar7 - _UNK_00760618;
  fVar11 = fVar10 - _UNK_0076061c;
  fVar16 = (((fVar16 - _DAT_00760650 * fVar2) - _DAT_00760640 * fVar2) - _DAT_00760630 * fVar2) -
           _DAT_00760620 * fVar2;
  fVar2 = (((fVar17 - _UNK_00760654 * fVar5) - _UNK_00760644 * fVar5) - _UNK_00760634 * fVar5) -
          _UNK_00760624 * fVar5;
  fVar17 = (((fVar25 - _UNK_00760658 * fVar8) - _UNK_00760648 * fVar8) - _UNK_00760638 * fVar8) -
           _UNK_00760628 * fVar8;
  fVar5 = (((fVar26 - _UNK_0076065c * fVar11) - _UNK_0076064c * fVar11) - _UNK_0076063c * fVar11) -
          _UNK_0076062c * fVar11;
  fVar25 = fVar16 * fVar16;
  fVar8 = fVar2 * fVar2;
  fVar26 = fVar17 * fVar17;
  fVar11 = fVar5 * fVar5;
  uVar18 = (uint)fVar1 & (uint)PTR_DAT_007605e0;
  uVar19 = (uint)fVar4 & (uint)PTR_DAT_007605e4;
  uVar21 = (uint)fVar7 & (uint)PTR_DAT_007605e8;
  uVar23 = (uint)fVar10 & (uint)PTR_DAT_007605ec;
  uVar3 = uVar18 & _DAT_007605d0;
  uVar6 = uVar19 & _UNK_007605d4;
  uVar9 = uVar21 & _UNK_007605d8;
  uVar12 = uVar23 & _UNK_007605dc;
  uVar20 = uVar19 - uVar6 & _UNK_007605c4;
  uVar22 = uVar21 - uVar9 & _UNK_007605c8;
  uVar24 = uVar23 - uVar12 & _UNK_007605cc;
  uVar27 = uVar18 + uVar3 & _DAT_007605c0;
  uVar28 = uVar19 + uVar6 & _UNK_007605c4;
  uVar21 = uVar21 + uVar9 & _UNK_007605c8;
  uVar23 = uVar23 + uVar12 & _UNK_007605cc;
  uVar19 = -(uint)((float)(uVar3 << 0x1e) != 0.0);
  uVar6 = -(uint)((float)(uVar6 << 0x1e) != 0.0);
  uVar9 = -(uint)((float)(uVar9 << 0x1e) != 0.0);
  uVar12 = -(uint)((float)(uVar12 << 0x1e) != 0.0);
  fVar16 = (((_DAT_00760600 * fVar25 + _DAT_007605b0) * fVar25 + _DAT_00760590) * fVar25 +
           _DAT_00760570) * fVar16;
  fVar2 = (((_UNK_00760604 * fVar8 + _UNK_007605b4) * fVar8 + _UNK_00760594) * fVar8 + _UNK_00760574
          ) * fVar2;
  fVar17 = (((_UNK_00760608 * fVar26 + _UNK_007605b8) * fVar26 + _UNK_00760598) * fVar26 +
           _UNK_00760578) * fVar17;
  fVar5 = (((_UNK_0076060c * fVar11 + _UNK_007605bc) * fVar11 + _UNK_0076059c) * fVar11 +
          _UNK_0076057c) * fVar5;
  fVar1 = (((_DAT_007605f0 * fVar25 + _DAT_007605a0) * fVar25 + _DAT_00760580) * fVar25 +
          _DAT_00760560) * fVar25 + _DAT_00760550;
  fVar4 = (((_UNK_007605f4 * fVar8 + _UNK_007605a4) * fVar8 + _UNK_00760584) * fVar8 + _UNK_00760564
          ) * fVar8 + _UNK_00760554;
  fVar25 = (((_UNK_007605f8 * fVar26 + _UNK_007605a8) * fVar26 + _UNK_00760588) * fVar26 +
           _UNK_00760568) * fVar26 + _UNK_00760558;
  fVar7 = (((_UNK_007605fc * fVar11 + _UNK_007605ac) * fVar11 + _UNK_0076058c) * fVar11 +
          _UNK_0076056c) * fVar11 + _UNK_0076055c;
  *param_2 = (~uVar19 & (uint)fVar16 | uVar19 & (uint)fVar1) ^
             (uVar18 - uVar3 & _DAT_007605c0) << 0x1e ^ *param_1 & _DAT_00760670;
  param_2[1] = (~uVar6 & (uint)fVar2 | uVar6 & (uint)fVar4) ^ uVar20 << 0x1e ^ uVar13;
  param_2[2] = (~uVar9 & (uint)fVar17 | uVar9 & (uint)fVar25) ^ uVar22 << 0x1e ^ uVar14;
  param_2[3] = (~uVar12 & (uint)fVar5 | uVar12 & (uint)fVar7) ^ uVar24 << 0x1e ^ uVar15;
  *param_3 = (uVar19 & (uint)fVar16 | ~uVar19 & (uint)fVar1) ^ uVar27 << 0x1e;
  param_3[1] = (uVar6 & (uint)fVar2 | ~uVar6 & (uint)fVar4) ^ uVar28 << 0x1e;
  param_3[2] = (uVar9 & (uint)fVar17 | ~uVar9 & (uint)fVar25) ^ uVar21 << 0x1e;
  param_3[3] = (uVar12 & (uint)fVar5 | ~uVar12 & (uint)fVar7) ^ uVar23 << 0x1e;
  return;
}

